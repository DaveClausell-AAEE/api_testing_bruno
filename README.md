Metodología de Pruebas de Sistemas

API de Gestión de Productos & Testing con Bruno

Este proyecto es la base práctica para la cátedra. Aquí encontrarás una API desarrollada en Python (Flask) y una colección de pruebas para realizar testing de caja negra.

Recurso Principal: Infografía Interactiva

Antes de empezar, consultá nuestra guía visual con todos los comandos necesarios:

👉 Link: https://daveclausell-aaee.github.io/api_testing_bruno/guia_testing.html

Requisitos Previos

Instalar Bruno: Descargá el cliente de pruebas desde: https://www.usebruno.com/

Instalar Docker: Descargá Docker Desktop para Windows.

WSL 2: Asegurate de tener habilitado WSL 2 en tu sistema.

Configuración del Entorno (Docker)

Seguí estos pasos en tu terminal (PowerShell o CMD):

1. Crear carpeta de trabajo

mkdir C:\sandbox

2. Lanzar el contenedor

docker run -it ^
  --privileged ^
  --name sandbox-estudiante ^
  -p 5000:5000 ^
  -v C:\sandbox:/home/sandbox ^
  debian


3. Configuración interna (Dentro de Debian)

apt update && apt install -y python3 python3-pip python3-venv git


4. Clonar el repositorio

cd /home/sandbox
git clone [https://github.com/DaveClausell-AAEE/api_testing_bruno.git](https://github.com/DaveClausell-AAEE/api_testing_bruno.git)
cd api_testing_bruno


Cómo correr el Servidor

Ejecutá estos comandos dentro de la carpeta del proyecto en el contenedor:

Instalar librerías:
pip install -r requirements.txt --break-system-packages

Ejecutar API:
python3 app.py

Nota: No cierres esta terminal, el servidor debe estar encendido.

Cómo usar Bruno para las Pruebas

Abrí Bruno en Windows.

Hacé clic en "Open Collection".

Buscá la carpeta: C:\sandbox\api_testing_bruno\pruebas-api

Seleccioná la carpeta y usá el botón "Send" para probar contra http://localhost:5000

Auxilio: ¿Se cerró la terminal?

Si el contenedor se detiene, usá este comando para volver a entrar:

docker start -ai sandbox-estudiante

Docente: Dave Clausell 
