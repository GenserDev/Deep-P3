import os
import re
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

RUTA = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(RUTA, "config.json")) as f:
    CONFIG = json.load(f)

SISTEMA = ("Eres un experto en MySQL 8. Con el esquema dado escribe una sola consulta SELECT "
           "que responda la pregunta. Responde solo con la consulta SQL, sin explicaciones.")

tokenizer = None
modelo = None


def cargar(usar_adapter=None, adapter=None):
    """Carga el modelo base y si se pide el adapter LoRA."""
    global tokenizer, modelo
    if usar_adapter is None:
        usar_adapter = CONFIG["usar_adapter"]
    adapter = adapter or os.path.join(RUTA, CONFIG["adapter"])
    # RUTA_MODELO permite usar una copia local del modelo base
    base = os.environ.get("RUTA_MODELO", CONFIG["modelo_base"])
    torch.manual_seed(CONFIG["semilla"])
    if torch.cuda.is_available():
        dispositivo, tipo = "cuda", torch.float16
    else:
        dispositivo, tipo = "cpu", torch.bfloat16
    tokenizer = AutoTokenizer.from_pretrained(base)
    modelo = AutoModelForCausalLM.from_pretrained(base, dtype=tipo).to(dispositivo)
    if usar_adapter:
        modelo = PeftModel.from_pretrained(modelo, adapter)
    modelo.eval()


def compactar_esquema(esquema):
    """Quita del esquema lo que no ayuda a escribir la consulta para que el prompt sea corto."""
    salida = []
    for linea in esquema.splitlines():
        linea = linea.strip().replace("`", "")
        if not linea:
            continue
        if linea.startswith("CREATE TABLE"):
            salida.append(linea)
            cuerpo = []
        elif linea.startswith(")"):
            comentario = re.search(r"COMMENT='(.*)'", linea)
            salida.append(",\n".join(cuerpo))
            salida.append(f") COMMENT='{comentario.group(1)}';" if comentario else ");")
        elif linea.startswith(("KEY", "UNIQUE KEY", "INDEX", "FULLTEXT")):
            continue
        elif linea.startswith("CONSTRAINT"):
            fk = re.search(r"FOREIGN KEY \((.*?)\) REFERENCES (\S+) \((.*?)\)", linea)
            cuerpo.append(f"  FOREIGN KEY ({fk.group(1)}) REFERENCES {fk.group(2)}({fk.group(3)})")
        else:
            linea = linea.rstrip(",")
            for patron in [r" NOT NULL", r" NULL", r" AUTO_INCREMENT", r" DEFAULT ('[^']*'|\S+)",
                           r" CHARACTER SET \S+", r" COLLATE \S+", r" ON UPDATE \S+"]:
                linea = re.sub(patron, "", linea)
            cuerpo.append("  " + linea)
    return "\n".join(salida)


def armar_mensajes(esquema, pregunta, sql_previo=None, error=None):
    texto = f"Esquema:\n{compactar_esquema(esquema)}\n\nPregunta: {pregunta}"
    if sql_previo:
        texto += f"\n\nEsta consulta dio un error:\n{sql_previo}\nError: {error}\nEscribe una consulta corregida."
    return [{"role": "system", "content": SISTEMA}, {"role": "user", "content": texto}]


def armar_prompt(mensajes):
    # enable_thinking=False desactiva el modo de razonamiento de Qwen3
    return tokenizer.apply_chat_template(mensajes, tokenize=False, add_generation_prompt=True, enable_thinking=False)


def limpiar_sql(texto):
    texto = texto.replace("```sql", "").replace("```", "").strip()
    texto = texto.split(";")[0].strip()
    inicio = re.search(r"\b(WITH|SELECT)\b", texto, re.IGNORECASE)
    if inicio:
        texto = texto[inicio.start():]
    return texto + ";"


def generar(mensajes, max_tokens=200):
    entrada = tokenizer(armar_prompt(mensajes), return_tensors="pt").to(modelo.device)
    with torch.no_grad():
        salida = modelo.generate(**entrada, max_new_tokens=max_tokens, do_sample=False,
                                 pad_token_id=tokenizer.eos_token_id)
    nuevo = salida[0][entrada["input_ids"].shape[1]:]
    return limpiar_sql(tokenizer.decode(nuevo, skip_special_tokens=True))


def generar_sql(esquema: str, pregunta: str, ejecutar=None) -> str:
    if modelo is None:
        cargar()
    sql = generar(armar_mensajes(esquema, pregunta))
    if ejecutar is None:
        return sql
    # Si la consulta falla se le muestra el error al modelo y se pide otra (maximo 3 llamadas a ejecutar)
    for _ in range(2):
        resultado = ejecutar(sql)
        if resultado["ok"]:
            return sql
        sql = generar(armar_mensajes(esquema, pregunta, sql, resultado["error"]))
    return sql
