# Funciones para crear las bases en MySQL y generar pares pregunta SQL
import random
import datetime
import pymysql

from esquemas import ESQUEMAS, ESQUEMAS_VALIDACION

CONEXION = dict(host="127.0.0.1", port=3306, user="root", password="root", charset="utf8mb4")
FEMENINOS = {"facultades", "inscripciones", "habitaciones", "funciones", "sedes", "clases",
             "canciones", "ordenes", "reparaciones", "asignaciones"}


def conectar(base=None):
    return pymysql.connect(database=base, autocommit=True, **CONEXION)


# ---------- creacion de las bases ----------

def ddl_tabla(tabla, pks):
    lineas = []
    pk = None
    fks = []
    for nombre, tipo, clase, desc, extra in tabla["cols"]:
        if clase == "pk":
            pk = nombre
            lineas.append(f"  `{nombre}` {tipo} NOT NULL AUTO_INCREMENT COMMENT '{desc}'")
        else:
            lineas.append(f"  `{nombre}` {tipo} NOT NULL COMMENT '{desc}'")
        if clase == "fk":
            fks.append((nombre, extra))
    lineas.append(f"  PRIMARY KEY (`{pk}`)")
    for col, ref in fks:
        lineas.append(f"  FOREIGN KEY (`{col}`) REFERENCES `{ref}` (`{pks[ref]}`)")
    comentario = tabla["comentario"] or tabla["desc"]
    return f"CREATE TABLE `{tabla['nombre']}` (\n" + ",\n".join(lineas) + f"\n) COMMENT='{comentario}'"


def valor_aleatorio(rng, clase, extra, tablas_n):
    if clase in ("txt", "cat"):
        return rng.choice(extra)
    if clase == "int":
        return rng.randint(extra[0], extra[1])
    if clase == "dec":
        return round(rng.uniform(extra[0], extra[1]), 2)
    if clase == "fecha":
        inicio = datetime.date(extra[0], 1, 1)
        fin = datetime.date(extra[1], 12, 31)
        return inicio + datetime.timedelta(days=rng.randint(0, (fin - inicio).days))
    if clase == "fk":
        # algunos padres quedan sin hijos para que tengan sentido las preguntas con NOT EXISTS
        return rng.randint(1, max(1, int(tablas_n[extra] * 0.9)))


def crear_base(nombre, tablas, semilla=2026):
    rng = random.Random(semilla)
    con = conectar()
    cur = con.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS `{nombre}`")
    cur.execute(f"CREATE DATABASE `{nombre}`")
    cur.execute(f"USE `{nombre}`")
    tablas_n = {t["nombre"]: t["n"] for t in tablas}
    pks = {t["nombre"]: t["cols"][0][0] for t in tablas}
    for tabla in tablas:
        cur.execute(ddl_tabla(tabla, pks))
        cols = [c for c in tabla["cols"] if c[2] != "pk"]
        filas = [[valor_aleatorio(rng, c[2], c[4], tablas_n) for c in cols] for _ in range(tabla["n"])]
        nombres = ", ".join(f"`{c[0]}`" for c in cols)
        marcas = ", ".join(["%s"] * len(cols))
        cur.executemany(f"INSERT INTO `{tabla['nombre']}` ({nombres}) VALUES ({marcas})", filas)
    con.close()


def esquema_texto(base):
    # Devuelve el esquema tal como lo entrega SHOW CREATE TABLE
    con = conectar(base)
    cur = con.cursor()
    cur.execute("SHOW TABLES")
    tablas = [f[0] for f in cur.fetchall()]
    partes = []
    for t in tablas:
        cur.execute(f"SHOW CREATE TABLE `{t}`")
        partes.append(cur.fetchone()[1] + ";")
    con.close()
    return "\n\n".join(partes)


def ejecutar_sql(base, sql, limite=None):
    con = conectar(base)
    cur = con.cursor()
    try:
        cur.execute(sql)
        filas = cur.fetchall()
        columnas = [d[0] for d in cur.description] if cur.description else []
        return {"ok": True, "columnas": columnas, "filas": list(filas)[:limite] if limite else list(filas), "error": None}
    except Exception as e:
        return {"ok": False, "columnas": [], "filas": [], "error": str(e)}
    finally:
        con.close()


# ---------- generacion de preguntas ----------

class Generador:
    def __init__(self, base, tablas, rng):
        self.base = base
        self.tablas = tablas
        self.rng = rng
        self.por_nombre = {t["nombre"]: t for t in tablas}

    def cols(self, tabla, *clases):
        return [c for c in tabla["cols"] if c[2] in clases]

    def pk(self, tabla):
        return self.cols(tabla, "pk")[0][0]

    def art(self, tabla):
        primera = tabla["desc"].split()[0]
        return "las" if primera.endswith("as") or primera in FEMENINOS else "los"

    def T(self, tabla):
        return self.art(tabla) + " " + tabla["desc"]

    def nombrar(self, col):
        # A veces se usa el nombre de la columna y a veces su descripcion
        return col[0] if self.rng.random() < 0.4 else col[3]

    def devuelve(self, cols):
        textos = [self.nombrar(c) for c in cols]
        if len(textos) == 1:
            return f"Devuelve {textos[0]}."
        return "Devuelve " + ", ".join(textos[:-1]) + " y " + textos[-1] + "."

    def valores(self, tabla, col):
        r = ejecutar_sql(self.base, f"SELECT DISTINCT `{col}` FROM `{tabla['nombre']}`")
        return [f[0] for f in r["filas"]]

    def umbral(self, tabla, col):
        vals = sorted(self.valores(tabla, col))
        v = vals[int(len(vals) * self.rng.uniform(0.3, 0.7))]
        return int(v) if not isinstance(v, int) else v

    def relaciones(self):
        # pares (hija, columna fk, padre)
        rel = []
        for t in self.tablas:
            for c in self.cols(t, "fk"):
                rel.append((t, c, self.por_nombre[c[4]]))
        return rel

    def etiqueta(self, tabla):
        # columna que identifica a una fila de forma legible
        txt = self.cols(tabla, "txt")
        return txt[0] if txt else self.cols(tabla, "pk")[0]

    def pk_ref(self, padre):
        return self.pk(padre)

    # ----- nivel facil -----

    def facil(self):
        t = self.rng.choice(self.tablas)
        n, tx = t["nombre"], self.T(t)
        nums = self.cols(t, "int", "dec")
        cats = self.cols(t, "cat")
        txts = self.cols(t, "txt")
        fechas = self.cols(t, "fecha")
        visibles = self.cols(t, "txt", "cat", "int", "dec", "fecha")
        r = self.rng
        tipo = r.randint(1, 11)
        if tipo == 1 and len(visibles) >= 2:
            c = r.sample(visibles, 2)
            q = r.choice([f"Muestra {self.nombrar(c[0])} y {self.nombrar(c[1])} de todos {tx}.",
                          f"Lista todos {tx} con sus columnas {c[0][0]} y {c[1][0]}."])
            return q, f"SELECT {c[0][0]}, {c[1][0]} FROM {n};"
        if tipo == 2 and cats and visibles:
            cat = r.choice(cats)
            v = r.choice(self.valores(t, cat[0]))
            c = r.choice([x for x in visibles if x != cat] or visibles)
            q = r.choice([f"Lista {tx} cuyo valor de {cat[3]} sea '{v}'. {self.devuelve([c])}",
                          f"¿Qué {t['desc']} tienen {cat[0]} igual a '{v}'? {self.devuelve([c])}"])
            return q, f"SELECT {c[0]} FROM {n} WHERE {cat[0]} = '{v}';"
        if tipo == 3 and nums:
            num = r.choice(nums)
            v = self.umbral(t, num[0])
            et = self.etiqueta(t)
            op, palabra = r.choice([(">", "mayor que"), ("<", "menor que"), (">=", "mayor o igual a")])
            q = r.choice([f"¿Qué {t['desc']} tienen {num[3]} {palabra} {v}? {self.devuelve([et, num])}",
                          f"Muestra {tx} con {num[0]} {palabra} {v}. {self.devuelve([et, num])}"])
            return q, f"SELECT {et[0]}, {num[0]} FROM {n} WHERE {num[0]} {op} {v};"
        if tipo == 4:
            if cats and r.random() < 0.6:
                cat = r.choice(cats)
                v = r.choice(self.valores(t, cat[0]))
                q = f"¿Cuántos registros de {t['desc']} tienen {cat[3]} igual a '{v}'? Devuelve una columna llamada total."
                return q, f"SELECT COUNT(*) AS total FROM {n} WHERE {cat[0]} = '{v}';"
            q = r.choice([f"¿Cuántos {t['desc']} hay en total? Devuelve una columna llamada total.",
                          f"Cuenta el numero de registros en la tabla {n}. Devuelve total."])
            return q, f"SELECT COUNT(*) AS total FROM {n};"
        if tipo == 5 and nums:
            num = r.choice(nums)
            fn, palabra = r.choice([("AVG", "promedio"), ("MAX", "valor maximo"), ("MIN", "valor minimo"), ("SUM", "suma total")])
            q = r.choice([f"¿Cuál es el {palabra} de {num[3]} en {tx}? Devuelve una columna llamada resultado.",
                          f"Calcula el {palabra} de la columna {num[0]} de la tabla {n}. Devuelve resultado."])
            return q, f"SELECT {fn}({num[0]}) AS resultado FROM {n};"
        if tipo == 6 and nums:
            num = r.choice(nums)
            et = self.etiqueta(t)
            k = r.choice([3, 5, 10])
            orden, palabra = r.choice([("DESC", "mayor"), ("ASC", "menor")])
            q = f"Muestra {self.nombrar(et)} y {self.nombrar(num)} de {k} {t['desc']} con {palabra} {num[3]}, ordenados de {palabra} a {'menor' if palabra == 'mayor' else 'mayor'}."
            return q, f"SELECT {et[0]}, {num[0]} FROM {n} ORDER BY {num[0]} {orden} LIMIT {k};"
        if tipo == 7 and cats:
            cat = r.choice(cats)
            q = r.choice([f"¿Qué valores distintos de {cat[3]} existen en {tx}? Devuelve {cat[0]}.",
                          f"Lista sin repetir los valores de {cat[0]} en la tabla {n}."])
            return q, f"SELECT DISTINCT {cat[0]} FROM {n};"
        if tipo == 8 and txts:
            tc = r.choice(txts)
            vals = [str(x) for x in self.valores(t, tc[0])]
            letra = r.choice(vals)[0]
            q = f"Lista {tx} cuyo {tc[3]} empieza con la letra '{letra}'. Devuelve {tc[0]}."
            return q, f"SELECT {tc[0]} FROM {n} WHERE {tc[0]} LIKE '{letra}%';"
        if tipo == 9 and cats and nums:
            cat, num = r.choice(cats), r.choice(nums)
            v = r.choice(self.valores(t, cat[0]))
            u = self.umbral(t, num[0])
            et = self.etiqueta(t)
            q = f"Muestra {tx} con {cat[3]} '{v}' y {num[3]} mayor que {u}. {self.devuelve([et, cat, num])}"
            return q, f"SELECT {et[0]}, {cat[0]}, {num[0]} FROM {n} WHERE {cat[0]} = '{v}' AND {num[0]} > {u};"
        if tipo == 10 and nums:
            num = r.choice(nums)
            a, b = sorted([self.umbral(t, num[0]), self.umbral(t, num[0])])
            et = self.etiqueta(t)
            q = f"¿Qué {t['desc']} tienen {num[3]} entre {a} y {b}? {self.devuelve([et, num])}"
            return q, f"SELECT {et[0]}, {num[0]} FROM {n} WHERE {num[0]} BETWEEN {a} AND {b};"
        if tipo == 11 and fechas:
            f = r.choice(fechas)
            v = r.choice(self.valores(t, f[0]))
            et = self.etiqueta(t)
            palabra, op = r.choice([("despues del", ">"), ("antes del", "<")])
            q = f"Lista {tx} con {f[3]} {palabra} {v}. {self.devuelve([et, f])}"
            return q, f"SELECT {et[0]}, {f[0]} FROM {n} WHERE {f[0]} {op} '{v}';"
        return None

    # ----- nivel medio -----

    def media(self):
        r = self.rng
        rel = self.relaciones()
        tipo = r.randint(1, 8)
        if tipo in (1, 2, 5, 6, 7, 8) and rel:
            h, fk, p = r.choice(rel)
            hn, pn = h["nombre"], p["nombre"]
            pk = self.pk(p)
            ep = self.etiqueta(p)
            nums_h = self.cols(h, "int", "dec")
            vis_h = self.cols(h, "cat", "int", "dec", "fecha", "txt")
            if tipo == 1 and vis_h:
                c = r.choice(vis_h)
                q = f"Muestra cada registro de {h['desc']} con su {c[3]} y el {ep[3]} de su {fk[3]}. {self.devuelve([c, ep])}"
                return q, f"SELECT h.{c[0]}, p.{ep[0]} FROM {hn} h JOIN {pn} p ON h.{fk[0]} = p.{pk};"
            if tipo == 2 and self.cols(p, "cat"):
                cat = r.choice(self.cols(p, "cat"))
                v = r.choice(self.valores(p, cat[0]))
                c = r.choice(vis_h) if vis_h else fk
                q = f"Lista {self.T(h)} cuyo {fk[3]} tiene {cat[3]} igual a '{v}'. {self.devuelve([c])}"
                return q, f"SELECT h.{c[0]} FROM {hn} h JOIN {pn} p ON h.{fk[0]} = p.{pk} WHERE p.{cat[0]} = '{v}';"
            if tipo == 5:
                q = r.choice([f"¿Cuántos registros de {h['desc']} tiene cada uno de {self.T(p)}? Devuelve {ep[0]} y la cantidad como total. Incluye solo los que tienen al menos uno.",
                              f"Para cada {ep[3]}, cuenta los registros de {h['desc']}. Devuelve {ep[0]} y total."])
                return q, f"SELECT p.{ep[0]}, COUNT(*) AS total FROM {pn} p JOIN {hn} h ON h.{fk[0]} = p.{pk} GROUP BY p.{pk}, p.{ep[0]};"
            if tipo == 6 and nums_h:
                num = r.choice(nums_h)
                fn, palabra = r.choice([("SUM", "la suma"), ("AVG", "el promedio"), ("MAX", "el maximo")])
                q = f"Para cada uno de {self.T(p)}, calcula {palabra} de {num[3]} de sus {h['desc']}. Devuelve {ep[0]} y el resultado."
                return q, f"SELECT p.{ep[0]}, {fn}(h.{num[0]}) AS resultado FROM {pn} p JOIN {hn} h ON h.{fk[0]} = p.{pk} GROUP BY p.{pk}, p.{ep[0]};"
            if tipo == 7:
                k = r.choice([2, 3, 5, 8])
                q = f"¿Qué {p['desc']} tienen más de {k} registros en {h['desc']}? Devuelve {ep[0]} y la cantidad como total."
                return q, f"SELECT p.{ep[0]}, COUNT(*) AS total FROM {pn} p JOIN {hn} h ON h.{fk[0]} = p.{pk} GROUP BY p.{pk}, p.{ep[0]} HAVING COUNT(*) > {k};"
            if tipo == 8 and nums_h:
                num = r.choice(nums_h)
                k = r.choice([3, 5])
                q = f"¿Cuáles son {k} {p['desc']} con mayor suma de {num[3]} en {h['desc']}? Devuelve {ep[0]} y la suma como total, de mayor a menor."
                return q, f"SELECT p.{ep[0]}, SUM(h.{num[0]}) AS total FROM {pn} p JOIN {hn} h ON h.{fk[0]} = p.{pk} GROUP BY p.{pk}, p.{ep[0]} ORDER BY total DESC LIMIT {k};"
        t = r.choice(self.tablas)
        n = t["nombre"]
        cats = self.cols(t, "cat")
        nums = self.cols(t, "int", "dec")
        if tipo == 3 and cats:
            cat = r.choice(cats)
            q = r.choice([f"Para cada {cat[3]}, ¿cuántos registros hay en {t['desc']}? Devuelve {cat[0]} y total.",
                          f"Cuenta {self.T(t)} agrupados por {cat[0]}. Devuelve {cat[0]} y la cantidad como total."])
            return q, f"SELECT {cat[0]}, COUNT(*) AS total FROM {n} GROUP BY {cat[0]};"
        if tipo == 4 and cats and nums:
            cat, num = r.choice(cats), r.choice(nums)
            fn, palabra = r.choice([("AVG", "promedio"), ("SUM", "suma"), ("MAX", "maximo"), ("MIN", "minimo")])
            if r.random() < 0.5:
                q = f"Para cada valor de {cat[3]}, calcula el {palabra} de {num[3]} en {self.T(t)}. Devuelve {cat[0]} y resultado."
                return q, f"SELECT {cat[0]}, {fn}({num[0]}) AS resultado FROM {n} GROUP BY {cat[0]};"
            u = self.umbral(t, num[0])
            q = f"¿Qué valores de {cat[0]} tienen un {palabra} de {num[3]} mayor que {u}? Devuelve {cat[0]} y resultado."
            return q, f"SELECT {cat[0]}, {fn}({num[0]}) AS resultado FROM {n} GROUP BY {cat[0]} HAVING {fn}({num[0]}) > {u};"
        if tipo in (1, 2) and len(rel) >= 2:
            # tabla con dos llaves foraneas
            for h in self.tablas:
                fks = self.cols(h, "fk")
                if len(fks) >= 2:
                    a, b = r.sample(fks, 2)
                    pa, pb = self.por_nombre[a[4]], self.por_nombre[b[4]]
                    ea, eb = self.etiqueta(pa), self.etiqueta(pb)
                    q = f"Para cada registro de {h['desc']}, muestra el {ea[3]} de su {a[3]} y el {eb[3]} de su {b[3]}. Devuelve {ea[0]} y {eb[0]}."
                    return q, (f"SELECT a.{ea[0]}, b.{eb[0]} FROM {h['nombre']} h JOIN {pa['nombre']} a ON h.{a[0]} = a.{self.pk(pa)} "
                               f"JOIN {pb['nombre']} b ON h.{b[0]} = b.{self.pk(pb)};")
        return None

    # ----- nivel dificil -----

    def dificil(self):
        r = self.rng
        tipo = r.randint(1, 10)
        t = r.choice(self.tablas)
        n = t["nombre"]
        nums = self.cols(t, "int", "dec")
        cats = self.cols(t, "cat")
        fechas = self.cols(t, "fecha")
        et = self.etiqueta(t)
        rel = self.relaciones()
        if tipo == 1 and nums:
            num = r.choice(nums)
            palabra, op = r.choice([("mayor", ">"), ("menor", "<")])
            q = f"Lista {self.T(t)} cuyo {num[3]} es {palabra} que el promedio de toda la tabla. {self.devuelve([et, num])}"
            return q, f"SELECT {et[0]}, {num[0]} FROM {n} WHERE {num[0]} {op} (SELECT AVG({num[0]}) FROM {n});"
        if tipo == 2 and rel:
            h, fk, p = r.choice(rel)
            ep = self.etiqueta(p)
            q = r.choice([f"¿Qué {p['desc']} no tienen ningún registro en {h['desc']}? Devuelve {ep[0]}.",
                          f"Lista {self.T(p)} que no aparecen en la tabla {h['nombre']}. Devuelve {ep[0]}."])
            return q, f"SELECT {ep[0]} FROM {p['nombre']} WHERE {self.pk(p)} NOT IN (SELECT {fk[0]} FROM {h['nombre']});"
        if tipo == 3 and cats and nums:
            cat, num = r.choice(cats), r.choice(nums)
            q = f"Para cada {cat[3]}, muestra el registro de {t['desc']} con el {num[3]} más alto, incluyendo empates. Devuelve {cat[0]}, {et[0]} y {num[0]}."
            return q, (f"WITH ranking AS (SELECT {cat[0]}, {et[0]}, {num[0]}, RANK() OVER (PARTITION BY {cat[0]} ORDER BY {num[0]} DESC) AS posicion FROM {n}) "
                       f"SELECT {cat[0]}, {et[0]}, {num[0]} FROM ranking WHERE posicion = 1;")
        if tipo == 4 and rel:
            h, fk, p = r.choice(rel)
            nums_h = self.cols(h, "int", "dec")
            if nums_h:
                num = r.choice(nums_h)
                ep = self.etiqueta(p)
                q = f"Calcula el total de {num[3]} de cada uno de {self.T(p)} y muestra solo los que superan el promedio de esos totales. Devuelve {ep[0]} y total."
                return q, (f"WITH totales AS (SELECT {fk[0]}, SUM({num[0]}) AS total FROM {h['nombre']} GROUP BY {fk[0]}) "
                           f"SELECT p.{ep[0]}, t.total FROM totales t JOIN {p['nombre']} p ON t.{fk[0]} = p.{self.pk(p)} "
                           f"WHERE t.total > (SELECT AVG(total) FROM totales);")
        if tipo == 5 and nums:
            num = r.choice(nums)
            q = f"Muestra {et[0]}, {num[0]} y la posicion de cada registro de {t['desc']} en un ranking por {num[3]} de mayor a menor usando RANK. Devuelve {et[0]}, {num[0]} y posicion."
            return q, f"SELECT {et[0]}, {num[0]}, RANK() OVER (ORDER BY {num[0]} DESC) AS posicion FROM {n};"
        if tipo == 6 and fechas:
            f = r.choice(fechas)
            anio = r.choice(sorted({v.year for v in self.valores(t, f[0])}))
            q = r.choice([f"¿Cuántos registros de {t['desc']} tienen {f[3]} en el año {anio}? Devuelve total.",
                          f"Cuenta {self.T(t)} cuyo {f[0]} cae en {anio}. Devuelve una columna total."])
            return q, f"SELECT COUNT(*) AS total FROM {n} WHERE YEAR({f[0]}) = {anio};"
        if tipo == 7 and fechas:
            f = r.choice(fechas)
            q = f"Cuenta {self.T(t)} por año de {f[3]}. Devuelve anio y total ordenados por anio."
            return q, f"SELECT YEAR({f[0]}) AS anio, COUNT(*) AS total FROM {n} GROUP BY YEAR({f[0]}) ORDER BY anio;"
        if tipo == 8 and fechas and nums:
            f, num = r.choice(fechas), r.choice(nums)
            anio = r.choice(sorted({v.year for v in self.valores(t, f[0])}))
            if r.random() < 0.5:
                q = f"Para cada mes del año {anio}, calcula la suma de {num[3]} en {self.T(t)} según {f[3]}. Devuelve mes y total ordenados por mes."
                return q, f"SELECT MONTH({f[0]}) AS mes, SUM({num[0]}) AS total FROM {n} WHERE YEAR({f[0]}) = {anio} GROUP BY MONTH({f[0]}) ORDER BY mes;"
            q = f"Para cada mes de {anio}, muestra la suma de {num[3]} y el acumulado hasta ese mes según {f[3]}. Devuelve mes, total y acumulado ordenados por mes."
            return q, (f"WITH por_mes AS (SELECT MONTH({f[0]}) AS mes, SUM({num[0]}) AS total FROM {n} WHERE YEAR({f[0]}) = {anio} GROUP BY MONTH({f[0]})) "
                       f"SELECT mes, total, SUM(total) OVER (ORDER BY mes) AS acumulado FROM por_mes ORDER BY mes;")
        if tipo == 9 and cats:
            cat = r.choice(cats)
            q = f"Para cada {cat[3]}, calcula el porcentaje de registros de {t['desc']} respecto al total, redondeado a 2 decimales. Devuelve {cat[0]} y porcentaje."
            return q, f"SELECT {cat[0]}, ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM {n}), 2) AS porcentaje FROM {n} GROUP BY {cat[0]};"
        if tipo == 10 and rel:
            h, fk, p = r.choice(rel)
            ep = self.etiqueta(p)
            q = f"¿Qué {p['desc']} tienen más registros en {h['desc']} que el promedio por {p['desc']}? Devuelve {ep[0]} y total."
            return q, (f"WITH conteo AS (SELECT {fk[0]}, COUNT(*) AS total FROM {h['nombre']} GROUP BY {fk[0]}) "
                       f"SELECT p.{ep[0]}, c.total FROM conteo c JOIN {p['nombre']} p ON c.{fk[0]} = p.{self.pk(p)} "
                       f"WHERE c.total > (SELECT AVG(total) FROM conteo);")
        return None


def generar_pares(base, tablas, cantidad, semilla=2026):
    rng = random.Random(semilla)
    g = Generador(base, tablas, rng)
    pares = []
    niveles = [("facil", g.facil), ("media", g.media), ("dificil", g.dificil)]
    intentos = 0
    while len(pares) < cantidad and intentos < cantidad * 20:
        intentos += 1
        nivel, funcion = rng.choices(niveles, weights=[3, 4, 5])[0]
        par = funcion()
        if par:
            pares.append({"base": base, "nivel": nivel, "pregunta": par[0], "sql": par[1]})
    return pares


def validar_pares(pares):
    # Ejecuta cada consulta en MySQL y separa las validas de las descartadas
    validos, descartes, vistos = [], [], set()
    for p in pares:
        clave = (p["base"], p["pregunta"])
        if clave in vistos:
            descartes.append({**p, "motivo": "pregunta duplicada"})
            continue
        vistos.add(clave)
        r = ejecutar_sql(p["base"], p["sql"])
        if not r["ok"]:
            descartes.append({**p, "motivo": "error de ejecucion: " + r["error"][:120]})
        elif len(r["filas"]) == 0 or r["filas"] == [(None,)] or r["filas"] == [(0,)]:
            descartes.append({**p, "motivo": "resultado vacio"})
        else:
            validos.append(p)
    return validos, descartes
