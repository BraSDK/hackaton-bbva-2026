# Manual del candidato

Prueba técnica: mejora de la entrega de tarjetas.

## 1. Qué es

- Una prueba técnica individual: mejorarás la estrategia que despacha tarjetas bancarias con varios transportistas.
- Este repositorio contiene todo lo necesario:
  - [`PRUEBA_TECNICA.md`](PRUEBA_TECNICA.md): el ejercicio, cómo ejecutarlo y qué contiene la entrega.
  - [`REGLAS_PUBLICAS.md`](REGLAS_PUBLICAS.md): las reglas de negocio y la referencia del simulador.
  - [`EVALUACION.md`](EVALUACION.md): los requisitos y el cálculo de la nota.
  - [`FAQ.md`](FAQ.md): las preguntas frecuentes.

## 2. Fechas

- Publicación: [fecha de publicación].
- Duración: una semana.
- Cierre: [fecha de cierre].
- Se evalúa la rama `main` de tu repositorio tal como esté subida (`git push`) a las 07:00 (hora de Lima) del día
  siguiente al cierre. Lo que subas después no se tiene en cuenta.

## 3. Identificación

- Te identificamos por el correo con el que te inscribiste.
- Indica ese correo en el campo `candidate` de `submission/submission_manifest.json`.

## 4. Cómo empezar

1. Crea en tu cuenta de GitHub un repositorio privado y vacío, sin README, `.gitignore` ni licencia.
2. Clona el repositorio del reto:
   `git clone https://github.com/bbvaHackaton2026/BBVA-Hackaton-2026.git`
3. Entra en la carpeta `BBVA-Hackaton-2026` y apunta `origin` a tu repositorio:
   `git remote set-url origin https://github.com/<tu-usuario>/<tu-repositorio>.git`
4. Sube el contenido: `git push -u origin main`.
5. En tu repositorio, en Settings → Collaborators, añade la cuenta `bbvaHackaton2026`.
6. Envía el enlace de tu repositorio y tu correo de inscripción a [canal de entrega].
7. Comprueba que todo funciona. Necesitas Git y Python 3.11 o superior. Desde la raíz del repositorio:
   - `python run.py`
   - `python run_150k.py`
   - `python -m unittest discover -s tests -v`

## 5. Cómo trabajar

- Tu repositorio debe ser privado durante toda la prueba.
- No hagas fork del repositorio del reto ni abras pull requests contra él.
- Puedes usar otras ramas, pero solo se evalúa `main`.
- Haz commits y súbelos con frecuencia.
- Solo se ejecuta `submission/candidate_strategy.py`. El `candidate_strategy.py` de la raíz, que usan `run.py` y las
  pruebas, no se evalúa: antes del cierre, copia la versión final a `submission/`.
- Los cambios en el motor, las interfaces o los datos no forman parte de la solución.

## 6. Qué entregar

En la raíz de tu repositorio, en la rama `main`, una carpeta `submission/` con:

- `candidate_strategy.py`: tu solución, en su versión final.
- `generated_artifacts/`: pruebas, scripts y prototipos que hayas creado. Si está vacía, deja un archivo `.gitkeep`.
- `ai_conversations/`: las conversaciones completas con IA, incluidos los intentos fallidos.
- `STRATEGY.md`: qué cambiaste y por qué, qué mediste y qué limitaciones quedan. Hasta 2.500 palabras.
- `submission_manifest.json`: inventario de archivos y herramientas, con tu correo en `candidate`.

El detalle de cada elemento está en [`PRUEBA_TECNICA.md`](PRUEBA_TECNICA.md).

## 7. Uso de IA

- Puedes apoyarte en herramientas de IA.
- Guarda las conversaciones en `submission/ai_conversations/` y declara las ayudas en `STRATEGY.md`.
- Eres responsable de revisar, comprender y justificar lo que entregas.

## 8. Cómo se evalúa

- La evaluación es automática: se ejecuta tu estrategia en escenarios distintos de los ejemplos del repositorio.
- Los requisitos, el tiempo máximo por escenario, el equipo de evaluación y la puntuación están en
  [`EVALUACION.md`](EVALUACION.md).

## 9. Preguntas

- Escribe al grupo de consultas: [enlace del grupo]. Respondemos en [plazo de respuesta].
- Antes de preguntar, revisa [`FAQ.md`](FAQ.md): se actualiza con las consultas recibidas.
- Puedes preguntar por:
  - aclaraciones del enunciado o de las reglas publicadas;
  - problemas técnicos del repositorio, indicando los pasos y el error;
  - el proceso: fechas, repositorio y entrega.
- No se responden preguntas sobre la solución, la puntuación ni los escenarios de evaluación. No incluyas tu código
  en las preguntas.
- Ejemplos de preguntas válidas:
  - «Al ejecutar `python run.py` obtengo este error: […]. ¿Qué puedo revisar?»
  - «Si no tengo scripts adicionales, ¿qué pongo en `generated_artifacts/`?»
  - «¿Se evalúa solo la rama `main` de mi repositorio?»

## 10. Trabajo individual

- La prueba es individual.
- No compartas tu solución con otros participantes ni la publiques mientras la convocatoria esté abierta.
- Las reglas de autoría y copia están en [`EVALUACION.md`](EVALUACION.md).
