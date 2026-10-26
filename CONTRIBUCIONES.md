# Contribuciones

Integrantes: GenserDev y Hugo2049.

Areas de responsabilidad. GenserDev es responsable de los datos y de la validacion propia. Hugo2049 es responsable del entrenamiento y del analisis de errores.

| Tarea | Responsable | Evidencia |
|---|---|---|
| Estructura del repositorio, config.json y requirements.txt | GenserDev | commit "Estructura base del proyecto" |
| Diseno de los 12 esquemas de entrenamiento y los 2 de validacion | GenserDev | datos/esquemas.py |
| Generador de pares y validacion en MySQL 8.4.10 | GenserDev | datos/construir.py, notebooks/01_datos.ipynb |
| Dataset de entrenamiento y descartes | GenserDev | datos/entrenamiento.jsonl, datos/descartes.csv |
| 40 preguntas de validacion propia redactadas y revisadas en MySQL | GenserDev | datos/validacion_propia.json |
| Evaluador por ejecucion y categorias de error | GenserDev | evaluador.py |
| solucion.py con el prompt y la correccion con ejecutar | Hugo2049 | solucion.py |
| Entrenamiento de las configuraciones A y B de LoRA | Hugo2049 | notebooks/02_entrenamiento.ipynb, adapters/ |
| Curvas de loss y resumen de entrenamiento | Hugo2049 | resultados/curvas_loss.png, resultados/resumen_entrenamiento.csv |
| Baseline, experimento de inferencia y analisis de errores | Hugo2049 | notebooks/03_evaluacion.ipynb, resultados/validacion_propia.csv |
| Eleccion del adapter final | Hugo2049 | adapter/ |
| README, bitacora, presentacion y prediccion de EX | GenserDev | README.md, BITACORA.md, presentacion.pdf |
