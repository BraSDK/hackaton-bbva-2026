# Preguntas frecuentes

Este archivo se actualiza con las consultas que llegan al grupo de consultas. La versión vigente es la del repositorio
del reto.

## Repositorio y entrega

**¿Puedo hacer un fork del repositorio del reto?**
No. Crea un repositorio privado propio y sube allí el contenido, como indica el [manual](README.md).

**¿Qué rama se evalúa?**
La rama `main` de tu repositorio, tal como esté subida (`git push`) a las 07:00 (hora de Lima) del día siguiente al
cierre.

**¿Cómo doy acceso a mi repositorio?**
En tu repositorio, en Settings → Collaborators, añade la cuenta `bbvaHackaton2026`. La invitación caduca a los 7 días si
no se acepta; si caduca, vuelve a enviarla.

**¿Dónde va la carpeta `submission/`?**
En la raíz de tu repositorio, en la rama `main`. Su contenido se describe en [`PRUEBA_TECNICA.md`](PRUEBA_TECNICA.md).

**¿Qué pongo en el campo `candidate` de `submission_manifest.json`?**
El correo con el que te inscribiste.

**Si no tengo scripts adicionales, ¿qué pongo en `generated_artifacts/`?**
Un archivo `.gitkeep`, declarado en `submission_manifest.json`.

**¿Tengo que entregar las conversaciones con IA?**
Sí: completas, incluidos los intentos fallidos, en `submission/ai_conversations/`.

## Ejecución

**¿Qué versión de Python necesito?**
Python 3.11 o superior. El equipo de evaluación se describe en [`EVALUACION.md`](EVALUACION.md).

**¿Puedo usar bibliotecas externas, como numpy o pandas?**
No. El evaluador incorpora solo `candidate_strategy.py` y no instala dependencias: usa la biblioteca estándar de Python.
Para comprobarlo en tu equipo, ejecuta `python -S run.py`: así Python no carga las bibliotecas instaladas.

**¿Puedo crear procesos o hilos, o usar la red?**
No. Lo prohíben las reglas de ejecución de [`REGLAS_PUBLICAS.md`](REGLAS_PUBLICAS.md).

**`python run.py` termina con `INTEGRITY_ERROR`. ¿Qué reviso?**
Algún archivo protegido cambió. Puedes modificar `candidate_strategy.py` y añadir archivos nuevos, por ejemplo pruebas
en `tests/`, pero no modificar los archivos existentes. Restáuralos a su versión original o vuelve a clonar el
repositorio del reto.

**¿Los ejemplos públicos puntúan?**
No. `run.py` (5.000 tarjetas) y `run_150k.py` (150.000 tarjetas) son casos de desarrollo.

## Consultas

**¿Dónde envío una pregunta?**
Al grupo de consultas: [enlace del grupo]. Las respuestas útiles para todos se añaden a este archivo.
