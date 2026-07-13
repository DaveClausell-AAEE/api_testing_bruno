import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def introduccion():
    limpiar_pantalla()
    print("==========================================================")
    print(" 🚀              BIENVENIDO A: LA ODISEA                   🚀  ")
    print("==========================================================")
    print("\n[SISTEMA]: Alerta. La base de datos central ha sido corrompida.")
    print("Tu misión como Analista de QA es auditar los endpoints malditos,")
    print("vencer a los bugs conceptuales y salvar el proyecto antes del receso.")
    print("\n==========================================================")
    input("\nPresioná [ENTER] para iniciar el escaneo de la API...")

def combate_1():
    limpiar_pantalla()
    print("--- ENCUENTRO 1: EL ENDPOINT DESCONOCIDO ---")
    print("\nTe topás con un Guardián del Código que bloquea el camino.")
    print("Te muestra un script que ejecuta pruebas automatizadas sobre una API")
    print("buscando bugs de forma reactiva en el producto ya terminado.")
    print("\nEl Guardián ruge: '¿En qué área opera este analista?'")
    print("\n[1] QA (Quality Assurance) - ¡Prevenimos el error en el proceso!")
    print("[2] QC (Quality Control) - ¡Identificamos defectos en el producto terminado!")
    
    opcion = input("\nElige tu ataque (1 o 2): ")
    if opcion == "2":
        print("\n🟢 ¡GOLPE CRÍTICO! Justo en el Control de Calidad. El Guardián retrocede.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡FALLO EN EL TEST! El Guardián te contraataca. QA es preventivo, esto era QC.")
        input("\nPresioná una tecla para reintentar...")
        return False

def combate_2():
    limpiar_pantalla()
    print("--- ENCUENTRO 2: LA MUTACIÓN DEL INSECTICIDA ---")
    print("\nLlegás a la sala de servidores. Un enjambre de bugs idénticos te rodea.")
    print("Ejecutás tu suite de pruebas automatizadas por décima vez consecutiva.")
    print("¡Pero no detectas ningún bug nuevo! Los insectos se ríen de tus scripts fijos.")
    print("\n¿Qué principio del ISTQB te está destruyendo y cómo lo mitigás?")
    print("\n[1] La paradoja del pesticida. ¡Debo revisar y actualizar la suite de pruebas!")
    print("[2] Pruebas exhaustivas. ¡Debo probar absolutamente todas las combinaciones infinitas!")
    
    opcion = input("\nElige tu ataque (1 o 2): ")
    if opcion == "1":
        print("\n🟢 ¡IMPECABLE! Actualizás los scripts de prueba en caliente y desintegrás al enjambre.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡CRASH! Intentaste hacer pruebas exhaustivas y te quedaste sin memoria RAM. Era el Pesticida.")
        input("\nPresioná una tecla para reintentar...")
        return False

def combate_3():
    limpiar_pantalla()
    print("--- ENCUENTRO 3: EL FILTRADO EN EL HISTÓRICO ---")
    print("\nUn clon malicioso de Bruno aparece. Al tirar un GET general te devuelve")
    print("un JSON con 20 registros donde hay telemetrías sucias fuera de rango.")
    print("¿Cuál es la función técnica de un analista frente a este hallazgo?")
    print("\n[1] Corregir los floats e ints directamente en la base de datos de producción.")
    print("[2] Reportar la anomalía y auditar la falta de sanitización de entradas en el backend.")
    
    opcion = input("\nElige tu ataque (1 o 2): ")
    if opcion == "2":
        print("\n🟢 ¡CORRECTO! Identificás la vulnerabilidad en la integridad de los datos.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡ERROR DE ROLES! El tester reporta y blinda, no parchea código en caliente.")
        input("\nPresioná una tecla para reintentar...")
        return False

def combate_4():
    limpiar_pantalla()
    print("--- ENCUENTRO 4: LA RESPUESTA DE ÉXITO POST ---")
    print("\nTe enfrentás a la compuerta lógica del servidor. Al mandar un valor válido")
    print("por POST para persistir un nuevo registro, ¿cuál es el Status Code")
    print("teórico esperado más preciso según el protocolo REST?")
    print("\n[1] 200 OK")
    print("[2] 201 Created")
    
    opcion = input("\nElige tu ataque (1 o 2): ")
    if opcion == "2":
        print("\n🟢 ¡BLINDAJE HTTP! La compuerta se abre de par en par al detectar la creación del recurso.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡FALSO POSITIVO! El código 200 es genérico; para inserciones exitosas el ideal es 201.")
        input("\nPresioná una tecla para reintentar...")
        return False

def combate_5():
    limpiar_pantalla()
    print("--- ENCUENTRO 5: EL DESARROLLADOR A LA DEFENSIVA ---")
    print("\nLlegás al núcleo de la API. El Jefe Final, 'El Dev Estresado', bloquea el despliegue.")
    print("Le encontraste un bug crítico en las fronteras de Caja Negra.")
    print("Si lo reportás de forma confrontativa diciendo: 'Tu código no sirve', cerrará el repositorio.")
    print("\n¿Qué habilidad del tester debés activar para salvar el sprint?")
    print("\n[1] Fuerza bruta - Reportar el bug gritando y exigiendo fix inmediato en los canales de Slack.")
    print("[2] Comunicación asertiva - Enfocarme de forma neutral y factual en el defecto del producto.")
    
    opcion = input("\nElige tu ataque (1 o 2): ")
    if opcion == "2":
        print("\n🟢 ¡ÉXITO DE INTEGRACIÓN! El Dev entiende el reporte empático y neutral, y mergea el fix.")
        input("\nPresioná una tecla para ver los resultados...")
        return True
    else:
        print("\n🔴 ¡CRASH DE EQUIPO! Fricción en el proyecto. El Dev te desestima el bug por confrontación.")
        input("\nPresioná una tecla para reintentar...")
        return False

def juego():
    introduccion()
    if combate_1():
        if combate_2():
            if combate_3():
                if combate_4():
                    if combate_5():
                        limpiar_pantalla()
                        print("==========================================================")
                        print(" 🎉             ¡FELICITACIONES, ANALISTA!              🎉 ")
                        print("==========================================================")
                        print("\nHas blindado la API y ganado el derecho a un merecido receso.")
                        print("\n🗝 CLAVE SEGUNDO CUATRIMESTRE: RECESO26")
                        print("Guarda este código para desbloquear el próximo juego.")
                        print("==========================================================")
                        return
    print("\n☠ GAME OVER: El software llegó a producción con fallos críticos. A revisar la teoría.")

if __name__ == "__main__":
    juego()
