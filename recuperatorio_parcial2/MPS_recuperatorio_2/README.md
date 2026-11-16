# Recuperatorio Parcial 2 — Metodología de Pruebas de Sistemas (MPS)

**Modalidad:** Presencial en laboratorio (90 minutos)  
**Puntaje Total:** 10.0 Puntos Directos (Aprobación: >= 6.0 puntos)  
**Archivo de Entrega:** `MPS_recup2_nombre_apellido.pdf` (PDF único consolidado)

---

## Reglas de Entorno del Aula

* El entorno ya cuenta con `python3`, `pytest`, `bru` (Bruno CLI) y Jenkins operativos.
* **Prohibido utilizar `apt` o `apt-get`:** No intentes instalar paquetes del sistema. Para auditar procesos y puertos utilizá exclusivamente herramientas nativas (`ps aux`, `ss -tulpn`, `netstat -tulpn`, `pkill -9 -f`).
* Dentro de Jenkins utilizá siempre la variable `${WORKSPACE}` para referenciar el directorio del proyecto.

---

## Consigna y Cronograma de Ejecución

### Etapa 1: Inspección y Ejecución de Pruebas (00 – 20 min)
1. Verificá la estructura del repositorio clonado con `ls -la` y revisá `environments/local.bru`.
2. Ejecutá las pruebas de **caja blanca** con `pytest -v`. Identificá las dos excepciones internas de Python y sus líneas exactas en `app_telemetria.py`.
3. Levantá el servicio (`python3 app_telemetria.py &`) y ejecutá las pruebas de **caja negra** con `bru run --env local` (y opcionalmente `curl -i`).

### Etapa 2: Orquestación CI/CD y Quality Gate en Jenkins (20 – 50 min)
1. Configurá un Pipeline en Jenkins apuntando al `Jenkinsfile` del repositorio.
2. Ejecutá el build y verificá que las fallas detectadas disparen el **Quality Gate** marcando el estado final en **`FAILURE`** (rojo) sin interrumpir la etapa `post`.
3. **CHECKPOINT 1 EN VIVO:** Levantá la mano y mostrá al docente en tu pantalla el *Stage View* en rojo y el *Console Output* con las trazas de falla.

### Etapa 3: Limpieza de Procesos y Liberación de Puertos (50 – 65 min)
1. Detené cualquier proceso residual de Flask/Python (`pkill -9 -f app_telemetria.py`).
2. Comprobá que los puertos `5000` y `5001` estén libres mediante `ss -tulpn` o `ps aux | grep python3`.
3. **CHECKPOINT 2 EN VIVO:** Mostrá al docente en tu terminal la comprobación limpia de procesos y sockets.

### Etapa 4: Reportes de Incidentes Jira y Entrega PDF (65 – 90 min)
1. Completá las fichas `TEL-BUG-01` y `TEL-BUG-02` utilizando `PLANTILLA_REPORTE_JIRA.md` (sin dejar textos entre corchetes `[...]`).
2. Consolidá las capturas de pantalla (entorno, PyTest, Bruno, Stage View de Jenkins, terminal limpia) y las dos fichas Jira en un **único archivo PDF** llamado `MPS_recup2_nombre_apellido.pdf`.

---

## Rúbrica de Evaluación (10 Puntos Directos)

| Criterio | Puntaje Máximo | Descripción |
| :--- | :---: | :--- |
| **1. Entorno y Estructura** | **1.0 pto** | Validación de `ls -la`, `environments/local.bru` y rutas correctas (`${WORKSPACE}`). |
| **2. Pruebas PyTest y Bruno CLI** | **3.0 ptos** | Detección de ambos HTTP 500, análisis de causa raíz (`ValueError` y `KeyError`) y distinción caja blanca/negra. |
| **3. Orquestación CI/CD y Quality Gate** | **3.0 ptos** | Pipeline declarativo funcional en Jenkins con `catchError`, Stage View en `FAILURE` y validación en Checkpoint 1. |
| **4. Limpieza y Gestión de Puertos** | **1.0 pto** | Apagado limpio de procesos y verificación de puertos 5000/5001 libres en Checkpoint 2. |
| **5. Reportes de Incidentes (Jira)** | **2.0 ptos** | Fichas `TEL-BUG-01` y `TEL-BUG-02` completas con pasos numéricos, esperado/obtenido, severidad y evidencias. |

### Penalizaciones Directas
* **-1.0 punto:** Entrega fuera de nomenclatura `MPS_recup2_nombre_apellido.pdf` o en múltiples archivos separados.
* **-1.0 punto:** Omisión de capturas de pantalla obligatorias (especialmente el *Stage View* de Jenkins).
* **-1.5 puntos:** Exposición de credenciales o tokens sensibles.
