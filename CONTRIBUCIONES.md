# Contribuciones

Integrantes: Genser y Hugo.

Areas de responsabilidad. Genser es responsable de los datos y de la validacion propia. Hugo es responsable del entrenamiento y del analisis de errores.

| Tarea | Responsable | Evidencia |
|---|---|---|
| Estructura del repositorio, config.json y requirements.txt | Genser | config.json, requirements.txt |
| Diseno de los 12 esquemas de entrenamiento y los 2 de validacion | Genser | datos/esquemas.py |
| Generador de pares y validacion en MySQL 8.4.10 | Genser | datos/construir.py, notebooks/01_datos.ipynb |
| Dataset de entrenamiento y descartes | Genser | datos/entrenamiento.jsonl, datos/descartes.csv |
| 40 preguntas de validacion propia redactadas y revisadas en MySQL | Genser | datos/validacion_propia.json |
| Evaluador por ejecucion y categorias de error | Genser | evaluador.py |
| solucion.py con el prompt y la correccion con ejecutar | Hugo | solucion.py |
| Entrenamiento de las configuraciones A y B de LoRA | Hugo | notebooks/02_entrenamiento.ipynb, adapters/ |
| Curvas de loss y resumen de entrenamiento | Hugo | resultados/curvas_loss.png, resultados/resumen_entrenamiento.csv |
| Baseline, experimento de inferencia y analisis de errores | Hugo | notebooks/03_evaluacion.ipynb, resultados/validacion_propia.csv |
| Eleccion del adapter final | Hugo | adapter/ |
| README, bitacora, presentacion y prediccion de EX | Genser | README.md, BITACORA.md, presentacion.pdf |
