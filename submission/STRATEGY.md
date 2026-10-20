# Estrategia de Despacho - Hackathon BBVA 2026

## 1. Enfoque Principal
El objetivo de esta estrategia es asegurar el estricto cumplimiento de los requisitos obligatorios (0 infracciones de retención, 0 envíos no resueltos y un SLA menor al 6%), priorizando la satisfacción del cliente y la robustez del servicio en escenarios de alta carga, asumiendo un costo mayor como inversión operativa.

## 2. Lógica del Algoritmo

* **Agrupación Inteligente (Batching):** Se implementó una estructura basada en `defaultdict(list)` que agrupa automáticamente los envíos entrantes mediante la tupla `(delivery_cluster_id, zone, attempt_number, required_capabilities)`. Esto asegura que los lotes propuestos al motor siempre sean válidos.
* **Control de Retención (Modo Emergencia):** Para garantizar 0 infracciones de `voluntary_hold_breaches`, el algoritmo evalúa la antigüedad de las tarjetas en la cola. Si un envío lleva 30 minutos o más en estado `READY` (acercándose al límite de 45), entra en "Modo Emergencia" y es despachado en el primer vehículo disponible, sin esperar a llenar el lote.
* **Priorización de SLA:** Las tarjetas en la cola se ordenan en cada iteración priorizando su tiempo límite (`sla_deadline`). Si una tarjeta está a menos de 6 horas de vencer, se activa su despacho inmediato.
* **Gestión de la Flota (Upgrades Mensuales):** Para soportar los picos de demanda y evitar la falta de unidades (`NO_AVAILABLE_UNIT`), se implementó la compra agresiva de mejoras en el hook `on_monthly_planning`. Se adquieren vehículos extra (`EXTRA_UNIT`), capacidad (`EXPANDED_CAPACITY`) y velocidad (`SPEED_SHIFT`) para los tres transportistas con la tarifa base más económica.
* **Depuración de Memoria y Envíos Zombis:** Para mantener bajo el consumo de memoria (RSS) y evitar bucles infinitos, cualquier envío rechazado por causas irreversibles (`TERMINAL_SHIPMENT`, `UNKNOWN_SHIPMENT`) es depurado de la cola inmediatamente.

## 3. Trabajo Futuro y Limitaciones
* Actualmente, el sistema invierte agresivamente en *Upgrades* mensuales. Una optimización futura incluiría calcular la tasa de utilización de la flota para comprar mejoras de forma dinámica solo cuando la proyección de demanda lo justifique, reduciendo así el "over_contingency_cents".
* El tamaño medio de lote (*average_batch_size*) es bajo debido a las reglas de emergencia que fuerzan despachos preventivos. Implementar una espera predictiva podría aumentar la eficiencia de agrupación.

## 4. Colaboración con IA y Declaración de Ayuda
* **Herramientas utilizadas:** Gemini (gemini-1.5-pro).
* **Descripción de la colaboración:** La IA se utilizó como *pair-programmer* para entender la compleja estructura de diccionarios anidados necesaria para cumplir con los requerimientos de `interfaces.py`, y para estructurar la lógica de retención obligatoria (límite de 45 minutos) descrita en `REGLAS_PUBLICAS.md`.
* **Proceso de validación:** El candidato dirigió la estrategia, revisó el código sugerido por la IA para evitar directivas legacy penalizables (ej. LEG-12) y verificó los resultados iterativamente ejecutando simulaciones locales (`run.py` y `run_150k.py`) analizando los reportes JSON para confirmar el éxito de las métricas.