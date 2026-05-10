🧪 Metodología de Pruebas de Sistemas

API de Gestión de Productos & Testing con Bruno

Este repositorio es la base práctica para la cátedra. Aquí encontrarás una API desarrollada en Python (Flask) y una colección de pruebas para realizar testing de caja negra.

📘 Recurso Principal: Infografía Interactiva

Antes de empezar, te recomendamos consultar nuestra guía visual con todos los comandos necesarios:

👉 VER INFOGRAFÍA DE LA MATERIA

🛠️ Requisitos Previos

Instalar Bruno: Descargá el cliente de pruebas desde su sitio oficial.

Instalar Docker: Descargá Docker Desktop para Windows.

WSL 2: Asegurate de tener habilitado WSL 2 en tu sistema.

🐳 Configuración del Entorno (Docker)

Seguí estos pasos en tu terminal (PowerShell o CMD) para crear un entorno de pruebas limpio:

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

Una vez dentro del contenedor, instalá las dependencias necesarias:

apt update && apt install -y python3 python3-pip python3-venv git


4. Clonar el repositorio

cd /home/sandbox
git clone [https://github.com/DaveClausell-AAEE/api_testing_bruno.git](https://github.com/DaveClausell-AAEE/api_testing_bruno.git)
cd api_testing_bruno


🚀 Cómo correr el Servidor

Para que la API esté disponible para las pruebas, debés ejecutar el siguiente comando dentro de la carpeta del proyecto en el contenedor:

Instalar librerías: pip install -r requirements.txt --break-system-packages

Ejecutar API: python3 app.py

Verás un mensaje que dice Running on http://0.0.0.0:5000. No cierres esta terminal, ya que el servidor debe estar encendido para poder testearlo.

🔍 Cómo usar Bruno para las Pruebas

Abrí la aplicación Bruno en Windows.

Hacé clic en "Open Collection".

Buscá en tu computadora la carpeta C:\sandbox\api_testing_bruno\pruebas-api y selecciónala.

Verás las peticiones preparadas. Hacé clic en "Send" para probar los endpoints contra http://localhost:5000.

🆘 Auxilio: ¿Se cerró la terminal?

Si cerraste la terminal por error, el contenedor se detiene. No uses docker run de nuevo, usá este comando para volver a entrar:

docker start -ai sandbox-estudiante

Docente: Dave Clausell
