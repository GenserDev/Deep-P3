# Proyecto 3. Texto a SQL con LoRA

Fine tuning con LoRA de un LLM pequeno para que, dado el esquema de una base de datos y una pregunta en espanol, genere una consulta MySQL correcta.

Integrantes: Genser y Hugo.

Modelo base: Qwen/Qwen3-1.7B con el modo de razonamiento desactivado.
Motor: MySQL 8.4.10 con su configuracion por defecto.

## Contenido del repositorio

| Ruta | Contenido |
|---|---|
| solucion.py | Carga el modelo de config.json y define generar_sql |
| config.json | Modelo base, adapter, uso del adapter y semilla |
| requirements.txt | Librerias necesarias |
| adapter/ | Adapter LoRA elegido |
| adapters/ | Las dos configuraciones entrenadas, A con r=8 y B con r=16 |
| evaluador.py | Comparacion por ejecucion y categorias de error |
| datos/esquemas.py | Definicion de los 12 esquemas de entrenamiento y los 2 de validacion |
| datos/construir.py | Crea las bases en MySQL y genera los pares pregunta SQL |
| datos/entrenamiento.jsonl | 2630 pares validos de entrenamiento |
| datos/descartes.csv | Pares descartados con su motivo |
| datos/validacion_propia.json | 40 preguntas de validacion propia |
| datos/esquemas_sql/ | Salida de SHOW CREATE TABLE de cada base |
| notebooks/01_datos.ipynb | Construccion y revision de los datos |
| notebooks/02_entrenamiento.ipynb | Entrenamiento de las configuraciones A y B |
| notebooks/03_evaluacion.ipynb | Baseline, configuraciones, experimento de inferencia y errores |
| resultados/ | validacion_propia.csv, resumenes y graficas |
| presentacion.pdf | Presentacion de 12 diapositivas |

## Como ejecutar

En Google Colab con GPU T4:

```
!git clone https://github.com/GenserDev/Deep-P3
%cd Deep-P3
!pip install -r requirements.txt
```

```python
import solucion
sql = solucion.generar_sql(esquema, "¿Cuántos clientes hay en Mixco?")
```

El modelo se carga la primera vez que se llama a generar_sql, o antes con `solucion.cargar()`. Con `"usar_adapter": false` en config.json se usa el modelo base con el mismo prompt. Si se tiene una copia local del modelo base se puede indicar con la variable de entorno `RUTA_MODELO`.

La funcion `ejecutar` es opcional. Si se pasa y la consulta da error en MySQL, el modelo recibe el error y escribe una consulta corregida. Se hacen como maximo 2 llamadas a `ejecutar`.

Para repetir los notebooks hace falta MySQL 8.4.10, por ejemplo con Docker:

```
docker run -d --name mysql84 -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql:8.4.10
```

Luego se corren los notebooks en orden: 01_datos, 02_entrenamiento y 03_evaluacion.

## Resumen de resultados

Exactitud por ejecucion ponderada (EX) en las 40 preguntas de validacion propia:

| Corrida | EX | Aciertos | Faciles | Medias | Dificiles |
|---|---|---|---|---|---|
| Baseline sin adapter | 0.620 | 27 de 40 | 11 de 13 | 10 de 15 | 6 de 12 |
| A con r=8 | 0.544 | 24 de 40 | 11 de 13 | 7 de 15 | 6 de 12 |
| B con r=16 | 0.570 | 25 de 40 | 11 de 13 | 8 de 15 | 6 de 12 |
| B con correccion usando ejecutar | 0.570 | 25 de 40 | 11 de 13 | 8 de 15 | 6 de 12 |

Entrenamiento:

| Config | r | Parametros entrenables | Minutos | Loss final | Loss en validacion |
|---|---|---|---|---|---|
| A | 8 | 8,716,288 | 53.8 | 0.020 | 0.246 |
| B | 16 | 17,432,576 | 41.7 | 0.023 | 0.237 |

El adapter elegido es B porque tuvo mejor EX que A. Las dos configuraciones bajaron mucho la loss en validacion, de 0.80 a cerca de 0.24, pero eso no se tradujo en mas aciertos. El adapter salio por debajo del modelo base.

El analisis de errores muestra la causa principal. Nuestras plantillas siempre agrupan por la llave primaria junto con el nombre, por ejemplo GROUP BY id, nombre. El modelo aprendio ese patron y lo repite cuando la pregunta pide agrupar por otra columna, como especie o motivo. Eso da filas de mas y el resultado no coincide. Tambien subieron los errores de JOIN, donde el modelo une tablas por columnas equivocadas.

La correccion con ejecutar no cambio el EX. Solo arregla consultas que dan error en MySQL, y casi todos los fallos son consultas que corren pero devuelven otro resultado.

Errores por categoria:

| Categoria | Baseline | A | B | B con ejecutar |
|---|---|---|---|---|
| JOIN | 2 | 3 | 5 | 5 |
| agregacion | 2 | 1 | 2 | 2 |
| columna o tabla inexistente | 1 | 4 | 1 | 0 |
| filtro | 0 | 1 | 0 | 0 |
| resultado distinto | 7 | 7 | 7 | 8 |
| sintaxis | 1 | 0 | 0 | 0 |

Para mejorar, el siguiente paso es variar la forma de las consultas en las plantillas, agrupar por la columna que pide la pregunta, y entrenar en GPU con todo el dataset.

## Prediccion de EX en la evaluacion oculta

Prediccion con adapter: EX entre 0.45 y 0.55.

Prediccion sin adapter: EX entre 0.50 y 0.60.

En validacion propia el base saco 0.62 y el adapter B saco 0.57.

La evaluacion oculta tiene mas tablas (5 a 10) y nombres que no vimos, por eso esperamos algo menos.

El adapter aprendio a agrupar por la llave primaria, que es el patron de nuestras plantillas.

Eso falla cuando la pregunta agrupa por otra columna, y en la evaluacion oculta pasara igual.

Por eso no esperamos mejora sobre el modelo base con este adapter.

## Limitaciones

Entrenamos sin GPU, en una CPU de 4 nucleos. Por eso cada configuracion uso 300 de los 2630 pares durante una epoca. El dataset completo esta en el repositorio y se puede usar para entrenar mas en Colab.

Las preguntas de entrenamiento salen de plantillas, asi que su redaccion es menos variada que la de una persona. La validacion propia se redacto aparte, con preguntas mas naturales, para medir esto.

## Licencias

Qwen/Qwen3-1.7B tiene licencia Apache 2.0. Las librerias usadas, transformers, peft, accelerate, torch y pymysql, tienen licencias abiertas. Los esquemas, datos y preguntas de este repositorio son propios y no vienen de Spider ni de BIRD.

## Uso de IA

Usamos un asistente de IA, Claude, para ayudar a escribir el codigo del generador de datos, las plantillas de preguntas, solucion.py, el evaluador y los notebooks, y para redactar la documentacion. Las 40 preguntas de validacion las redactamos con ayuda del asistente y las revisamos una por una ejecutandolas en MySQL. Las decisiones del proyecto, la revision de resultados y la entrega son responsabilidad del equipo.
