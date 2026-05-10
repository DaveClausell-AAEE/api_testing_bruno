API de Productos - CÃ¡tedra de Pruebas
Este proyecto es para practicar pruebas de sistemas con Bruno.

# Instalar Bruno #

[Bruno](https://www.usebruno.com/)

# Instalar DOCKER #

1- Instalar [Docker](https://docs.docker.com/desktop/setup/install/windows-install/) Desktop.

2- Tener habilitado [ WSL 2](https://docs.docker.com/desktop/setup/install/windows-install/#wsl-verification-and-setup/)

# Crear carpeta de trabajo #

Abri una terminal (PowerShell o CMD) y crea una carpeta para persistir tus archivos. Esto evitara¡que tu trabajo se borre al apagar el contenedor:

1- mkdir C:\sandbox.

# Crear y lanzar el contenedor #

Copia y pega este comando en la terminal:

docker run -it ^
  --privileged ^
  --name sandbox-estudiante ^
  -p 5000:5000 ^
  -v C:\sandbox:/home/sandbox ^
  debian

# Dentro del contenedor #
# Configuracion #
Ya dentro del contenedor (vas a ver que el promt cambio) instala las siguientes dependencias:

apt update && apt install -y python3 python3-pip python3-venv git

# Clonar el repositorio #

cd /home/sandbox
git clone https://github.com/DaveClausell-AAEE/api_testing_bruno.git
cd api_testing_bruno
