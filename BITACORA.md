# Bitacora

Horas en tiempo de Guatemala.

## 2026-10-25 15:05. GenserDev
Revisamos el enunciado y el entorno de trabajo. No tenemos GPU, solo CPU de 4 nucleos con soporte bfloat16. Levantamos MySQL 8.4.10 con la imagen de Docker mysql:8.4.10. Elegimos Qwen/Qwen3-1.7B como modelo base, con el modo de razonamiento desactivado.

## 2026-10-25 15:10. GenserDev
Disenamos 12 esquemas de entrenamiento y 2 de validacion. Mezclamos nombres en espanol, en ingles y abreviados, y pusimos COMMENT en todas las columnas porque asi viene el esquema en la evaluacion oculta.

## 2026-10-25 15:15. GenserDev
Escribimos el generador de pares con plantillas en tres niveles. Cada consulta se ejecuta en MySQL y solo se guardan las que corren sin error. Resultado: 5400 pares generados, 2630 validos y 2770 descartados. Casi todos los descartes son preguntas repetidas y 36 son consultas con resultado vacio.

## 2026-10-25 15:15. Hugo2049
Medimos la velocidad de entrenamiento en CPU. Un ejemplo de unos 400 tokens tarda entre 4 y 7 segundos con LoRA. Por eso decidimos entrenar cada configuracion con una muestra del dataset y no con todo.

## 2026-10-25 15:20. GenserDev
Redactamos las 40 preguntas de validacion sobre los esquemas veterinaria y airline, con 13 faciles, 15 medias y 12 dificiles. Revisamos que todas las consultas de referencia devuelvan filas y que ninguna tabla de validacion este en el entrenamiento.

## 2026-10-25 15:20. Hugo2049
Escribimos solucion.py. El esquema se compacta antes de ponerlo en el prompt para que sea mas corto. Quitamos ENGINE, CHARSET, indices y NOT NULL, pero dejamos tipos, llaves y COMMENT. Agregamos la correccion con ejecutar cuando MySQL devuelve un error.

## 2026-10-25 15:30. Hugo2049
Primer intento de entrenamiento con 800 ejemplos por configuracion. El contenedor se reinicio antes de terminar y se perdio el avance. Lo volvimos a lanzar guardando el resultado de cada configuracion al terminar. Por tiempo bajamos a 300 ejemplos por configuracion.

## 2026-10-25 18:37. Hugo2049
Termino la configuracion A en 54 minutos. La loss de entrenamiento bajo a 0.02 y la loss en validacion propia bajo de 0.80 a 0.25. La configuracion B iba muy lenta porque la memoria del modelo A no se libero. Reiniciamos el proceso para B y agregamos en solucion.py una linea que libera el modelo anterior antes de cargar otro.

## 2026-10-25 20:20. Hugo2049
Evaluamos baseline, configuracion A, configuracion B y el experimento de correccion con ejecutar sobre la validacion propia. El baseline saco EX 0.62, A saco 0.544 y B saco 0.57. La correccion con ejecutar no cambio el resultado. El adapter salio peor que el modelo base porque copio el patron de agrupar por la llave primaria que tienen nuestras plantillas. Elegimos B como adapter final.

## 2026-10-25 20:35. GenserDev
Escribimos el README, la presentacion y la prediccion de EX para la evaluacion oculta. Generamos historial_git.txt.
