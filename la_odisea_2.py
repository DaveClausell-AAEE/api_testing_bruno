import os
import sys
import random

# Lista oficial de 30 números de 5 cifras para validación de cátedra
CODIGOS_VALIDACION = [
    14852, 15926, 19283, 21974, 23581, 28374, 29631, 31415, 32715, 35749,
    37465, 41258, 42187, 43859, 50692, 54921, 58963, 61803, 63214, 65103,
    72419, 74125, 76294, 83951, 85236, 87315, 94102, 96325, 98420, 10583
]

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_acceso():
    limpiar_pantalla()
    print("==========================================================")
    print(" 🛰️             LA ODISEA - PARTE 2: EL REGRESO          🛰️ ")
    print("==========================================================")
    print("\n[SISTEMA]: Módulo de Seguridad activado.")
    print("Para desbloquear los servidores de la segunda mitad del año,")
    print("debés ingresar la clave alfanumérica de 8 dígitos obtenida en la Parte 1.")
    print("==========================================================")
    
    clave = input("\n🔑 Ingrese la clave de acceso: ").strip()
    
    if clave == "RECESO26":
        print("\n🟢 ACCESO CONCEDIDO. Sincronizando entornos Docker y colecciones de Bruno...")
        input("\nPresioná [ENTER] para iniciar la Fase de Auditoría...")
        return True
    else:
        print("\n🔴 ACCESO DENEGADO. Código de protocolo inválido. El sistema se autodestruirá.")
        print("💡 Tip de Cátedra: Revisá el código final que te dio el juego anterior antes del receso.")
        sys.exit()

def presentar_opciones_aleatorias(opciones_dict):
    lista_opciones = list(opciones_dict.items())
    random.shuffle(lista_opciones)
    
    indice_correcto = None
    for i, (texto, es_correcta) in enumerate(lista_opciones, start=1):
        print(f"[{i}] {texto}")
        if es_correcta:
            indice_correcto = str(i)
            
    return indice_correcto

def desafio_1():
    limpiar_pantalla()
    print("--- ⚔️ DESAFÍO 1: EL CONTRATO DE INTEGRACIÓN CRÍTICO ---")
    print("\nEstás auditando un endpoint POST que registra la telemetría del Rover.")
    print("El desarrollador te dice que el test pasa porque devuelve un 201 Created.")
    print("Sin embargo, al revisar el JSON de respuesta de Bruno, notás que el body")
    print("está completamente vacío `{}` en lugar de devolver el ID asignado.")
    print("\n¿Cuál es el veredicto técnico correcto basándote en la teoría de pruebas?\n")
    
    opciones = {
        "El test es un FALSO NEGATIVO. La API funciona bien, el problema es de Bruno.": False,
        "El test es un FALSO POSITIVO. El Status Code es correcto, pero se viola el contrato del JSON.": True,
        "El test es un PASS total. Si el código es 201, la persistencia está asegurada.": False
    }
    
    correcto = presentar_opciones_aleatorias(opciones)
    opcion = input("\nElige tu respuesta: ")
    
    if opcion == correcto:
        print("\n🟢 ¡IMPECABLE! Detectaste el bug invisible. El código de estado no lo es todo; la estructura importa.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡BOOM! Te comiste el falso positivo en producción. El software fallará al leer datos vacíos.")
        input("\nPresioná una tecla para reintentar...")
        return False

def desafio_2():
    limpiar_pantalla()
    print("--- ⚔️ DESAFÍO 2: SINTAXIS AVANZADA CHAI.JS ---")
    print("\nNecesitás automatizar un test en la pestaña 'Tests' de Bruno.")
    print("El objetivo es asegurar que la respuesta que viene del servidor")
    print("sea estrictamente un formato Objeto JSON (Estructurado) para que no rompa la app.")
    print("\n¿Cuál es la aserción lógicas en JavaScript correcta usando Chai.js?\n")
    
    opciones = {
        "expect(res.getBody()).to.equal('json');": False,
        "expect(res.getBody()).to.be.an('object');": True,
        "assert.isTrue(res.body == 'Object');": False
    }
    
    correcto = presentar_opciones_aleatorias(opciones)
    opcion = input("\nElige tu respuesta: ")
    
    if opcion == correcto:
        print("\n🟢 ¡LUZ VERDE (PASS)! Automatización perfecta. El tipo de dato está blindado de forma nativa.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡LUZ ROJA (FAIL)! Error de sintaxis en JavaScript. Rompiste la suite de pruebas.")
        input("\nPresioná una tecla para reintentar...")
        return False

def desafio_3():
    limpiar_pantalla()
    print("--- ⚔️ DESAFÍO 3: CAJA NEGRA Y ANÁLISIS EXTREMO DE FRONTERAS ---")
    print("\nUn nuevo sensor de presión opera en un rango ultra restrictivo:")
    print("De 600 a 900 Pa inclusive. Si aplicás la técnica de Análisis de Valores Límite (BVA),")
    print("un analista senior debe elegir valores contiguos inmediatamente fuera de la frontera.")
    print("\n¿Qué par de valores representan exactamente los límites excluidos inválidos?\n")
    
    opciones = {
        "600 y 900": False,
        "601 y 899": False,
        "599 y 901": True
    }
    
    correcto = presentar_opciones_aleatorias(opciones)
    opcion = input("\nElige tu respuesta: ")
    
    if opcion == correcto:
        print("\n🟢 ¡GOLPE CRÍTICO EN LAS FRONTERAS! Evaluaste exactamente el borde externo ($600-1$ y $900+1$).")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡SISTEMA EXPUESTO! Probaste valores que están dentro del rango seguro o en la frontera exacta.")
        input("\nPresioná una tecla para reintentar...")
        return False

def desafio_4():
    limpiar_pantalla()
    print("--- ⚔️ DESAFÍO 4: PERFORMANCE Y ROBUSTEZ EN LA API ---")
    print("\nEl requerimiento no funcional de la misión exige alta velocidad.")
    print("Debés programar un test que valide que el backend del Rover Curiosity")
    print("responda las consultas en un tiempo menor a los 200 milisegundos.")
    print("\n¿Qué propiedad nativa del objeto de respuesta de Bruno debés auditar?\n")
    
    opciones = {
        "res.responseTime": True,
        "res.getSpeed()": False,
        "res.headers['X-Time']": False
    }
    
    correcto = presentar_opciones_aleatorias(opciones)
    opcion = input("\nElige tu respuesta: ")
    
    if opcion == correcto:
        print("\n🟢 ¡CÓDIGO EFICIENTE! Capturás los milisegundos de respuesta de la API de forma exacta.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡TIMEOUT! Consultaste una propiedad inexistente mientras el servidor se degradaba.")
        input("\nPresioná una tecla para reintentar...")
        return False

def desafio_5():
    limpiar_pantalla()
    print("--- ⚔️ DESAFÍO 5: LA PRUEBA EXHAUSTIVA IMPOSIBLE ---")
    print("\nEl Gerente de Proyecto, apurado por el despliegue a producción, te dice:")
    print("'Probá todas las combinaciones de números reales (floats) posibles en el endpoint")
    print("así nos aseguramos de que no tenga ningún bug antes de lanzar'.")
    print("\nBasándote en los principios fundamentales del ISTQB, ¿qué le respondés?\n")
    
    opciones = {
        "'Excelente idea, armo un bucle infinito en Python para probar los millones de floats'.": False,
        "'Es imposible. Las pruebas exhaustivas no se pueden hacer. Debemos usar Particiones de Equivalencia y Valores Límite'.": True,
        "'No hace falta probar floats, con meter dos cadenas de texto (Strings) ya cubrimos la seguridad'.": False
    }
    
    correcto = presentar_opciones_aleatorias(opciones)
    opcion = input("\nElige tu respuesta: ")
    
    if opcion == correcto:
        print("\n🟢 ¡CRITERIO ACADÉMICO PROFESIONAL! Defendiste los principios del testing con rigor universitario.")
        input("\nPresioná una tecla para avanzar...")
        return True
    else:
        print("\n🔴 ¡PROYECTO CAÍDO! Te quedaste atrapado en un bucle infinito intentando probar infinitos números.")
        input("\nPresioná una tecla para reintentar...")
        return False

def desafio_6():
    limpiar_pantalla()
    print("--- ⚔️ DESAFÍO FINAL: AUDITORÍA DE BIBLIOGRAFÍA OFICIAL ---")
    print("\nPara desactivar de forma definitiva la corrupción del Rover, debés")
    print("demostrar que tenés el programa oficial del ISTQB abierto y analizado.")
    print("\nBusca el documento 'ISTQB_CTFL_Syllabus-v4.0-ES.pdf' en el Classroom.")
    print("Ubicá la sección donde describe qué es el 'Análisis de Valores Límite'.")
    print("¿Cuál es la última palabra del 4to párrafo de esa descripción?")
    
    palabra = input("\n✍️ Escribí la palabra exacta (en minúsculas): ").strip().lower()
    if palabra == "porcentaje":
        print("\n🟢 ¡VERIFICACIÓN DE CÁTEDRA COMPLETA! Has demostrado un dominio analítico y teórico total.")
        input("\nPresioná una tecla para reclamar tu recompensa...")
        return True
    else:
        print("\n🔴 ¡ERROR DE LECTURA! Esa no es la palabra que figura al cierre del 4to párrafo. Revisá el Syllabus.")
        input("\nPresioná una tecla para reintentar...")
        return False

def juego():
    if verificar_acceso():
        if desafio_1():
            if desafio_2():
                if desafio_3():
                    if desafio_4():
                        if desafio_5():
                            if desafio_6():
                                # Selección aleatoria de un código de 5 cifras
                                codigo_secreto = random.choice(CODIGOS_VALIDACION)
                                
                                limpiar_pantalla()
                                print("==========================================================")
                                print(" 🎉 🎉 ¡FELICITACIONES, SENIOR TESTER MASTER CHIEF! 🎉 🎉 ")
                                print("==========================================================")
                                print("\n Has completado de forma perfecta LA ODISEA: PARTE 2.")
                                print(" Tu rigor conceptual y tus scripts en Bruno han salvado el semestre.")
                                print("\nAquí tenés tu reconocimiento oficial de la cátedra:\n")
                                print("          __________")
                                print("         '._==_==_=_.'")
                                print("         .-\\:      /-.")
                                print(f"        | (|  {codigo_secreto}  |) |") # El código de 5 cifras se inserta acá
                                print("         '-|       |-'")
                                print("           \\       /")
                                print("            ':---:'")
                                print("            _|_|_")
                                print("           |_____|")
                                print("\n🏆 MEDALLA DE LA COPA AUTOMATION DESBLOQUEADA 🏆")
                                print(f"\n🔑 CÓDIGO DE VERIFICACIÓN DE FINALIZACIÓN: {codigo_secreto}")
                                print("\n¡Que disfrutes del merecido receso invernal sin bugs!")
                                print("==========================================================")
                                return
    print("\n☠️ GAME OVER: El software llegó a producción inestable. A repasar las aserciones.")

if __name__ == "__main__":
    juego()
