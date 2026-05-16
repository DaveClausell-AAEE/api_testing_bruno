# 🚀 Guía de Automatización: Jenkins + Bruno

Este documento contiene las instrucciones técnicas para configurar nuestro Pipeline de Integración Continua. El objetivo es que el "robot" (Jenkins) realice las pruebas de calidad automáticamente.

## 1. El archivo Jenkinsfile
Para que Jenkins sepa qué hacer, debemos crear un archivo llamado `Jenkinsfile` (sin extensión) en la **raíz de tu proyecto** (junto a `app.py`).

### Código del Pipeline
Copia y pega el siguiente código dentro de tu archivo `Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    tools {
        // Usa la instalación de Node que configuramos en Jenkins
        nodejs 'node20'
    }

    stages {
        stage('Checkout') {
            steps {
                // Descarga el código desde GitHub
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Instala las librerías necesarias para que la API funcione
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Run API') {
            steps {
                // Enciende la API en segundo plano
                sh 'python3 app.py &'
                // Espera 5 segundos para asegurar que el servidor subió
                sleep 5 
            }
        }

        stage('Execute Bruno Tests') {
            steps {
                // Corre los tests de Bruno de forma automatizada (CLI)
                sh 'bru run --collection ./bruno-collection'
            }
        }
    }
}

---
```

## 🎯 Tu Misión: El Desafío del Semáforo

1. [cite_start]**La Falla Inicial:** Al ejecutar el Pipeline por primera vez, verás que se pone en **ROJO** (Build Failed)[cite: 20]. [cite_start]Esto es correcto, ya que los tests detectarán los bugs que dejamos en la API[cite: 20].
2. **El Análisis:** Revisa los logs de Jenkins para ver qué test de Bruno falló.
3. [cite_start]**La Solución:** Corrige el error de lógica en tu archivo `app.py`[cite: 21].
4. [cite_start]**La Victoria:** Haz un `git push` con tu corrección[cite: 21]. [cite_start]Si Jenkins vuelve a correr y el semáforo cambia a **VERDE**, ¡el desafío está cumplido![cite: 21].
