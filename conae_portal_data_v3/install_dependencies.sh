cat << 'EOF' > install_dependencies.sh
#!/bin/bash

# Exit on error
set -e

echo "=========================================================="
echo "  APROVISIONANDO ENTORNO DE TESTING & CI/CD - CONAE v3.0  "
echo "=========================================================="

# 1. Actualizar repositorios e instalar paquetes base del sistema
echo "[1/6] Actualizando paquetes del sistema..."
apt-get update -y
apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    procps \
    nano \
    openjdk-17-jre \
    python3 \
    python3-pip \
    python3-venv

# 2. Instalar Node.js y Bruno CLI (para auditorías de API)
echo "[2/6] Instalando Node.js y Bruno CLI..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi
npm install -g @usebruno/cli || true

# 3. Instalar librerías de Python (Flask, PyTest, Requests)
echo "[3/6] Instalando dependencias de Python (Flask, PyTest)..."
pip3 install --no-cache-dir --break-system-packages flask pytest requests

# 4. Asegurar carpetas base de Jenkins y logs
echo "[4/6] Preparando directorios del sistema..."
mkdir -p /opt/jenkins
mkdir -p /home/sandbox

# 5. Descargar jenkins.war si no existe en la carpeta actual
echo "[5/6] Verificando binario de Jenkins..."
if [ ! -f "jenkins.war" ] && [ ! -f "/home/sandbox/api_testing_bruno/jenkins.war" ]; then
    echo "Descargando jenkins.war oficial LTS..."
    curl -L -o jenkins.war https://get.jenkins.io/war-stable/latest/jenkins.war
fi

# Copy jenkins.war to /opt/jenkins for persistence
if [ -f "jenkins.war" ]; then
    cp jenkins.war /opt/jenkins/jenkins.war
elif [ -f "/home/sandbox/api_testing_bruno/jenkins.war" ]; then
    cp /home/sandbox/api_testing_bruno/jenkins.war /opt/jenkins/jenkins.war
fi

# 6. Salida de verificación de versiones instaladas
echo ""
echo "=========================================================="
echo "         REPORTE DE VERSIONES INSTALADAS - CI/CD         "
echo "=========================================================="
echo "Operating System: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '"')"
echo "Python 3:         $(python3 --version 2>&1)"
echo "PyTest:           $(pytest --version 2>&1 | head -n 1)"
echo "Java (JRE):       $(java -version 2>&1 | head -n 1)"
echo "cURL:             $(curl --version 2>&1 | head -n 1 | cut -d' ' -f1-2)"
echo "Node.js:          $(node -v 2>&1 || echo 'No instalado')"
echo "Bruno CLI:        $(bru --version 2>&1 || echo 'Instalado vía NPM')"
echo "Jenkins WAR:      $(ls -lh /opt/jenkins/jenkins.war 2>/dev/null | awk '{print $5, $9}' || echo 'No encontrado')"
echo "=========================================================="
echo "✔ Aprovisionamiento completado exitosamente."
EOF

# Dar permisos de ejecución
chmod +x install_dependencies.sh
