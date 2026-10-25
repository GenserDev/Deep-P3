# Evaluador por ejecucion: compara el resultado de la consulta generada con el de la consulta de referencia
import re
import datetime
import itertools
from decimal import Decimal
from collections import Counter


def normalizar(valor):
    if isinstance(valor, (Decimal, float)):
        return round(float(valor), 2)
    if isinstance(valor, (datetime.date, datetime.datetime)):
        return str(valor)
    return valor


def comparar(ref, pred, ordenado=False):
    """True si pred contiene las columnas de ref con los mismos valores. Una columna extra no penaliza."""
    filas_ref = [tuple(normalizar(v) for v in f) for f in ref]
    filas_pred = [tuple(normalizar(v) for v in f) for f in pred]
    if len(filas_ref) != len(filas_pred):
        return False
    if not filas_ref:
        return True
    n_ref, n_pred = len(filas_ref[0]), len(filas_pred[0])
    # para cada columna de ref buscamos columnas de pred con los mismos valores
    candidatas = []
    for i in range(n_ref):
        col_ref = Counter(f[i] for f in filas_ref)
        cand = [j for j in range(n_pred) if Counter(f[j] for f in filas_pred) == col_ref]
        if not cand:
            return False
        candidatas.append(cand)
    for mapeo in itertools.product(*candidatas):
        if len(set(mapeo)) < n_ref:
            continue
        proyectado = [tuple(f[j] for j in mapeo) for f in filas_pred]
        if ordenado and proyectado == filas_ref:
            return True
        if not ordenado and Counter(proyectado) == Counter(filas_ref):
            return True
    return False


def es_solo_lectura(sql):
    return bool(re.match(r"^\s*(SELECT|WITH)\b", sql, re.IGNORECASE))


def categoria_error(sql_ref, sql_pred, error):
    """Clasifica un fallo en: sintaxis, columna o tabla inexistente, JOIN, agregacion, filtro o resultado distinto."""
    if error:
        if "1064" in error:
            return "sintaxis"
        if "1054" in error or "1146" in error:
            return "columna o tabla inexistente"
        if "1055" in error or "1111" in error or "group" in error.lower():
            return "agregacion"
        return "sintaxis"
    ref, pred = sql_ref.upper(), sql_pred.upper()
    if ref.count("JOIN") != pred.count("JOIN"):
        return "JOIN"
    agregados = ["GROUP BY", "HAVING", "COUNT(", "SUM(", "AVG(", "MAX(", "MIN(", "OVER ("]
    if any((a in ref) != (a in pred) for a in agregados):
        return "agregacion"
    if ("WHERE" in ref) != ("WHERE" in pred) or ref.count("WHERE") != pred.count("WHERE"):
        return "filtro"
    return "resultado distinto"
