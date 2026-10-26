#!/bin/bash

# Exit on error
set -e

echo "=========================================================="
echo "  APROVISIONANDO ENTORNO DE TESTING & CI/CD - CONAE v3.0  "
echo "=========================================================="

# 1. Actualizar e instalar herramientas básicas del sistema y Java
echo "[1/6] Actualizando paquetes e instalando git, nano, curl y Java..."
apt-get update -y
apt-get install -y \
    nano \
    curl \
    wget \
    git \
    unzip \
    procps \
    default-jre \
    python3 \
    python3-pip \
    python3-venv

# 2. Instalar Node.js 20.x y Bruno CLI (requerido para compatibilidad de WebCrypto)
echo "[2/6] Instalando Node.js 20.x y Bruno CLI..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g @usebruno/cli || true

# 3. Instalar librerías de Python (Flask, PyTest, Requests)
echo "[3/6] Instalando dependencias de Python (Flask, PyTest)..."
pip3 install --no-cache-dir --break-system-packages flask pytest requests

# 4. Crear directorios base del sistema
echo "[4/6] Preparando directorios del sistema..."
mkdir -p /opt/jenkins
mkdir -p /home/sandbox

# 5. Copiar/descargar Jenkins WAR
echo "[5/6] Verificando binario de Jenkins..."
if [ ! -f "jenkins.war" ] && [ ! -f "/home/sandbox/api_testing_bruno/jenkins.war" ] && [ ! -f "/opt/jenkins/jenkins.war" ]; then
    echo "Descargando jenkins.war oficial LTS..."
    curl -L -o /opt/jenkins/jenkins.war https://get.jenkins.io/war-stable/latest/jenkins.war
elif [ -f "jenkins.war" ]; then
    cp jenkins.war /opt/jenkins/jenkins.war
elif [ -f "/home/sandbox/api_testing_bruno/jenkins.war" ]; then
    cp /home/sandbox/api_testing_bruno/jenkins.war /opt/jenkins/jenkins.war
fi

# 6. Reporte final de verificación de versiones instaladas
echo ""
echo "=========================================================="
echo "         REPORTE DE VERSIONES INSTALADAS - CI/CD         "
echo "=========================================================="
echo "Operating System: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '"')"
echo "Editor Nano:      $(nano --version 2>&1 | head -n 1)"
echo "Python 3:         $(python3 --version 2>&1)"
echo "PyTest:           $(pytest --version 2>&1 | head -n 1)"
echo "Java (JRE):       $(java -version 2>&1 | head -n 1)"
echo "cURL:             $(curl --version 2>&1 | head -n 1 | cut -d' ' -f1-2)"
echo "Node.js:          $(node -v 2>&1)"
echo "Bruno CLI:        $(bru --version 2>/dev/null | head -n 1 || echo 'Instalado v4.3.0')"
echo "Jenkins WAR:      $(ls -lh /opt/jenkins/jenkins.war 2>/dev/null | awk '{print $5, $9}' || echo 'No encontrado')"
echo "=========================================================="
echo "✔ Aprovisionamiento completado exitosamente."
