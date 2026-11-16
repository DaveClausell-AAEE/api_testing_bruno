# Reporte de Incidentes (Estilo Jira) — Recuperatorio Parcial 2

> **Instrucciones:** Completá todos los campos entre corchetes y eliminá las marcas `[...]` antes de exportar a PDF.

---

## Ficha de Defecto #1: `TEL-BUG-01`

| Campo | Detalle |
| :--- | :--- |
| **ID del Incidente** | `TEL-BUG-01` |
| **Resumen / Título** | [Completar: ej. Error HTTP 500 por ValueError no capturado en GET /api/v1/telemetria] |
| **Componente / Archivo** | `app_telemetria.py` — Línea `[Completar número de línea]` |
| **Severidad / Prioridad** | `[Alta / Crítica]` |
| **Ambiente** | Servidor local Flask (`http://127.0.0.1:5001`) |

**Pasos para Reproducir:**
1. Iniciar el servicio ejecutando `python3 app_telemetria.py`.
2. Realizar una petición `GET` a `http://127.0.0.1:5001/api/v1/telemetria?orbita=abc`.
3. Inspeccionar el código de estado HTTP y la traza de error en consola/PyTest.

* **Resultado Esperado:** `[Completar qué código HTTP y respuesta JSON debería devolver la API]`
* **Resultado Obtenido:** `[Completar qué código HTTP devolvió y qué excepción de Python ocurrió]`
* **Análisis de Causa Raíz (Caja Blanca):** `[Explicar brevemente por qué falla la línea de código en app_telemetria.py]`
* **Evidencia:** `[Pegar aquí captura de pantalla de PyTest / Bruno / curl]`

---

## Ficha de Defecto #2: `TEL-BUG-02`

| Campo | Detalle |
| :--- | :--- |
| **ID del Incidente** | `TEL-BUG-02` |
| **Resumen / Título** | [Completar: ej. Error HTTP 500 por KeyError al omitir clave 'accion' en POST /api/v1/comando] |
| **Componente / Archivo** | `app_telemetria.py` — Línea `[Completar número de línea]` |
| **Severidad / Prioridad** | `[Alta / Crítica]` |
| **Ambiente** | Servidor local Flask (`http://127.0.0.1:5001`) |

**Pasos para Reproducir:**
1. Iniciar el servicio ejecutando `python3 app_telemetria.py`.
2. Enviar una petición `POST` a `http://127.0.0.1:5001/api/v1/comando` con header `Content-Type: application/json` y body `{"objetivo": "antena_principal"}`.
3. Observar el código de estado HTTP devuelto por el servidor.

* **Resultado Esperado:** `[Completar qué código HTTP y respuesta JSON debería devolver la API]`
* **Resultado Obtenido:** `[Completar qué código HTTP devolvió y qué excepción de Python ocurrió]`
* **Análisis de Causa Raíz (Caja Blanca):** `[Explicar brevemente por qué falla la indexación directa del diccionario]`
* **Evidencia:** `[Pegar aquí captura de pantalla de PyTest / Bruno / curl]`
