"""
==============================================================================
MÓDULO DE LÓGICA DEL JUEGO Y TEMPORIZADOR (juego.py)
==============================================================================
Este archivo contiene el flujo central de una partida de trivia:
1. Carga y validación de las preguntas desde el archivo JSON.
2. Selección al azar de preguntas según la categoría elegida.
3. Cronometraje de respuestas con el módulo estándar 'time'.
4. Cálculo de puntajes y bonificaciones/penalizaciones por velocidad.
5. Almacenamiento del historial de partidas en 'datos/usuarios.json'.

¿POR QUÉ SE USA TIME?
Usamos 'time.time()' antes y después del input() del usuario. Al restar ambos
valores obtenemos los segundos exactos transcurridos sin interrumpir abruptamente
al jugador en la consola, permitiendo penalizar la demora de manera limpia.
==============================================================================
"""

import os
import json
import random
import time
from datetime import datetime
import statistics

import interfaz
import estadisticas

# Constantes de configuración de la partida
RUTA_PREGUNTAS = os.path.join(os.path.dirname(__file__), "datos", "preguntas.json")
RUTA_USUARIOS = os.path.join(os.path.dirname(__file__), "datos", "usuarios.json")

TIEMPO_LIMITE_SEGUNDOS = 15.0  # Tiempo sugerido para responder cada pregunta
PUNTOS_BASE = 100              # Puntos base por respuesta correcta
BONO_POR_SEGUNDO = 10          # Puntos extra por cada segundo restante (si tiempo <= 15 s)
PENALIZACION_POR_SEGUNDO = 5   # Puntos descontados por cada segundo de retraso (si tiempo > 15 s)
PUNTOS_MINIMOS_ACIERTO = 30    # Puntaje mínimo garantizado por una respuesta correcta


def cargar_preguntas(ruta=RUTA_PREGUNTAS):
    """
    QUÉ HACE: Lee el archivo JSON con las preguntas y lo convierte en lista de Python.
    POR QUÉ: Centraliza la carga de datos y maneja posibles errores si el archivo no existe.
    """
    if not os.path.exists(ruta):
        interfaz.mostrar_mensaje_error(f"No se encontró el archivo de preguntas en: {ruta}")
        return []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            preguntas = json.load(f)
            if not isinstance(preguntas, list):
                interfaz.mostrar_mensaje_error("El formato del banco de preguntas es inválido.")
                return []
            return preguntas
    except json.JSONDecodeError:
        interfaz.mostrar_mensaje_error("Error al leer el archivo JSON de preguntas (archivo corrupto).")
        return []
    except Exception as e:
        interfaz.mostrar_mensaje_error(f"Error inesperado al cargar preguntas: {str(e)}")
        return []


def cargar_historial(ruta=RUTA_USUARIOS):
    """
    QUÉ HACE: Carga el historial de partidas desde 'usuarios.json'.
    Si el archivo no existe, lo crea automáticamente con una lista vacía [].
    POR QUÉ: Evita errores en la primera ejecución cuando todavía no se ha jugado ninguna partida.
    """
    # Si no existe la carpeta datos, la creamos
    carpeta_datos = os.path.dirname(ruta)
    if carpeta_datos and not os.path.exists(carpeta_datos):
        os.makedirs(carpeta_datos, exist_ok=True)

    if not os.path.exists(ruta):
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
            return []
        except Exception:
            return []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            historial = json.load(f)
            return historial if isinstance(historial, list) else []
    except (json.JSONDecodeError, Exception):
        # Si el archivo está vacío o dañado, devolvemos lista vacía
        return []


def guardar_partida(datos_partida, ruta=RUTA_USUARIOS):
    """
    QUÉ HACE: Añade la nueva partida al archivo JSON de historial.
    POR QUÉ: Permite persistir los datos para que el ranking y los reportes
    en Excel incluyan todas las partidas acumuladas.
    """
    historial = cargar_historial(ruta)
    historial.append(datos_partida)

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        interfaz.mostrar_mensaje_error(f"No se pudo guardar la partida: {str(e)}")
        return False


def pedir_nombre_jugador():
    """
    QUÉ HACE: Solicita el nombre del jugador y valida que no esté en blanco.
    POR QUÉ: Toda partida debe quedar registrada a nombre de alguien para el ranking.
    """
    while True:
        interfaz.consola.print("[bold yellow]Ingresa tu nombre o apodo:[/bold yellow] ", end="")
        nombre = input().strip()
        if nombre:
            return nombre
        interfaz.mostrar_mensaje_aviso("El nombre no puede estar vacío. Por favor ingresa al menos un caracter.")


def elegir_categoria():
    """
    QUÉ HACE: Muestra el menú de categorías y valida la selección del usuario.
    POR QUÉ: Permite al jugador elegir temática específica o jugar 'Mixto'.
    """
    categorias_mapa = {
        "1": "Cultura General",
        "2": "Ciencia",
        "3": "Historia",
        "4": "Deportes",
        "5": "Mixto"
    }

    while True:
        interfaz.limpiar_pantalla()
        interfaz.mostrar_banner()
        interfaz.mostrar_menu_categorias()

        interfaz.consola.print("[bold yellow]Selecciona una categoría (1 al 5):[/bold yellow] ", end="")
        opcion = input().strip()

        if opcion in categorias_mapa:
            return categorias_mapa[opcion]

        interfaz.mostrar_mensaje_error("Opción inválida. Debes ingresar un número del 1 al 5.")
        interfaz.pausar()


def elegir_cantidad_preguntas(max_disponibles):
    """
    QUÉ HACE: Permite al jugador elegir cuántas preguntas responder (5 o 10).
    POR QUÉ: Cumple con la especificación de cantidad configurable de preguntas.
    """
    while True:
        interfaz.consola.print(
            f"\n[bold yellow]¿Cuántas preguntas deseas jugar?[/bold yellow] "
            f"([bold green]5[/bold green] o [bold cyan]10[/bold cyan]) [dim][Enter para 5 por defecto][/dim]: ",
            end=""
        )
        entrada = input().strip()

        if entrada == "":
            return min(5, max_disponibles)

        if entrada in ["5", "10"]:
            cantidad = int(entrada)
            if cantidad > max_disponibles:
                interfaz.mostrar_mensaje_aviso(
                    f"Solo hay {max_disponibles} preguntas disponibles en esta categoría. Jugaremos {max_disponibles}."
                )
                return max_disponibles
            return cantidad

        interfaz.mostrar_mensaje_error("Por favor ingresa 5 o 10 (o presiona Enter para 5).")


def filtrar_preguntas(todas_preguntas, categoria_elegida):
    """
    QUÉ HACE: Filtra las preguntas del banco según la categoría elegida.
    Si la categoría es 'Mixto', devuelve todas las preguntas disponibles.
    """
    if categoria_elegida == "Mixto":
        return list(todas_preguntas)
    return [p for p in todas_preguntas if p.get("categoria") == categoria_elegida]


def calcular_puntos_pregunta(es_correcta, tiempo_segundos):
    """
    QUÉ HACE: Aplica el sistema de puntaje según acierto y velocidad:
    - Si falla: 0 puntos.
    - Si acierta en <= 15 s: 100 puntos base + (15 - tiempo) * 10 de bono de velocidad.
    - Si acierta en > 15 s: 100 puntos base - (tiempo - 15) * 5 de penalización (mínimo 30 pts).
    POR QUÉ: Premia el conocimiento y los reflejos rápidos, penalizando la tardanza.

    RETORNA:
        (int puntos, bool penalizado)
    """
    if not es_correcta:
        return 0, False

    if tiempo_segundos <= TIEMPO_LIMITE_SEGUNDOS:
        # Respuesta rápida: bono por cada segundo restante
        segundos_restantes = TIEMPO_LIMITE_SEGUNDOS - tiempo_segundos
        bono = int(segundos_restantes * BONO_POR_SEGUNDO)
        puntos = PUNTOS_BASE + bono
        return puntos, False
    else:
        # Respuesta lenta: penalización proporcional
        segundos_tarde = tiempo_segundos - TIEMPO_LIMITE_SEGUNDOS
        descuento = int(segundos_tarde * PENALIZACION_POR_SEGUNDO)
        puntos = max(PUNTOS_MINIMOS_ACIERTO, PUNTOS_BASE - descuento)
        return puntos, True


def iniciar_partida():
    """
    QUÉ HACE: Orquesta toda la partida de principio a fin:
    1. Carga el banco de preguntas.
    2. Pide datos del jugador y su categoría.
    3. Mezcla y selecciona preguntas con random.sample().
    4. Muestra cada pregunta, cronometra con time.time() y evalúa.
    5. Muestra retroalimentación con colores de Rich (verde, amarillo, rojo).
    6. Calcula estadísticas finales y las guarda en usuarios.json.
    """
    todas_preguntas = cargar_preguntas()
    if not todas_preguntas:
        interfaz.mostrar_mensaje_error("No hay preguntas disponibles para jugar.")
        interfaz.pausar()
        return

    interfaz.limpiar_pantalla()
    interfaz.mostrar_banner()

    # Paso 1: Pedir nombre del jugador
    jugador = pedir_nombre_jugador()

    # Paso 2: Elegir categoría
    categoria = elegir_categoria()

    # Paso 3: Filtrar preguntas según la categoría
    preguntas_filtradas = filtrar_preguntas(todas_preguntas, categoria)
    if not preguntas_filtradas:
        interfaz.mostrar_mensaje_error(f"No hay preguntas cargadas para la categoría '{categoria}'.")
        interfaz.pausar()
        return

    # Paso 4: Elegir cantidad de preguntas
    cantidad = elegir_cantidad_preguntas(len(preguntas_filtradas))

    # Paso 5: Seleccionar preguntas al azar usando random.sample
    # random.sample garantiza que no se repitan preguntas dentro de la misma partida
    preguntas_partida = random.sample(preguntas_filtradas, cantidad)

    # Variables acumuladoras de la partida
    puntaje_total = 0
    aciertos = 0
    tiempos_respuesta = []

    interfaz.limpiar_pantalla()
    interfaz.consola.print(
        f"\n[bold green]¡Todo listo, {jugador}![/bold green] "
        f"Comienza tu partida de [bold magenta]{categoria}[/bold magenta] ({cantidad} preguntas).\n"
    )
    interfaz.pausar()

    # Bucle principal de preguntas
    for i, datos_pregunta in enumerate(preguntas_partida, start=1):
        interfaz.limpiar_pantalla()
        interfaz.mostrar_pregunta(i, cantidad, datos_pregunta)

        # Iniciamos el cronómetro antes del input
        tiempo_inicio = time.time()

        # Bucle de validación para asegurar que el jugador elija 1, 2, 3 o 4
        while True:
            interfaz.consola.print("[bold yellow]Tu respuesta (1, 2, 3 o 4):[/bold yellow] ", end="")
            entrada = input().strip()

            if entrada in ["1", "2", "3", "4"]:
                opcion_elegida = int(entrada)
                break
            interfaz.mostrar_mensaje_error("Entrada inválida. Debes escribir el número de una de las opciones: 1, 2, 3 o 4.")

        # Detenemos el cronómetro justo después de que el usuario presiona Enter
        tiempo_fin = time.time()
        tiempo_transcurrido = round(tiempo_fin - tiempo_inicio, 1)
        tiempos_respuesta.append(tiempo_transcurrido)

        # Verificamos si la respuesta es correcta
        respuesta_correcta_num = datos_pregunta.get("respuesta_correcta", 1)
        opciones = datos_pregunta.get("opciones", [])
        texto_correcta = opciones[respuesta_correcta_num - 1] if 1 <= respuesta_correcta_num <= len(opciones) else ""

        es_correcta = (opcion_elegida == respuesta_correcta_num)

        # Calculamos los puntos y si hubo penalización por tardar más de 15s
        puntos_obtenidos, penalizado = calcular_puntos_pregunta(es_correcta, tiempo_transcurrido)
        puntaje_total += puntos_obtenidos

        if es_correcta:
            aciertos += 1

        # Mostramos el resultado visual con los colores requeridos (verde/amarillo/rojo)
        interfaz.mostrar_resultado_respuesta(
            es_correcta=es_correcta,
            tiempo_segundos=tiempo_transcurrido,
            puntos=puntos_obtenidos,
            penalizado=penalizado,
            texto_correcta=texto_correcta
        )

        interfaz.pausar()

    # Fin de la partida: calculamos estadísticas finales con el módulo estadisticas
    efectividad = estadisticas.calcular_efectividad(aciertos, cantidad)
    tiempo_promedio = round(statistics.mean(tiempos_respuesta), 1) if tiempos_respuesta else 0.0

    # Estructura del registro para guardar en JSON y exportar a Excel
    registro_partida = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jugador": jugador,
        "categoria": categoria,
        "puntaje": puntaje_total,
        "aciertos": aciertos,
        "total_preguntas": cantidad,
        "efectividad": efectividad,
        "tiempo_promedio": tiempo_promedio
    }

    # Guardamos en usuarios.json
    guardar_partida(registro_partida)

    # Mostramos resumen final
    interfaz.limpiar_pantalla()
    interfaz.mostrar_resumen_partida(
        jugador=jugador,
        categoria=categoria,
        puntaje=puntaje_total,
        aciertos=aciertos,
        total=cantidad,
        efectividad=efectividad,
        tiempo_promedio=tiempo_promedio
    )
    interfaz.pausar()
