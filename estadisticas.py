"""
==============================================================================
MÓDULO DE ESTADÍSTICAS Y RANKING (estadisticas.py)
==============================================================================
Este archivo realiza todos los cálculos numéricos y resúmenes de desempeño
utilizando la biblioteca estándar 'statistics' de Python.

¿POR QUÉ SE USA EL MÓDULO STATISTICS?
El módulo estándar 'statistics' proporciona funciones matemáticas optimizadas
como mean() (media o promedio aritmético) y mode() (moda o elemento más frecuente),
evitando reinventar la rueda y garantizando cálculos precisos y profesionales.
==============================================================================
"""

import statistics


def calcular_efectividad(aciertos, total_preguntas):
    """
    QUÉ HACE: Calcula el porcentaje de respuestas acertadas respecto al total.
    POR QUÉ: Permite medir el rendimiento del jugador sin importar si jugó 5 o 10 preguntas.
    FÓRMULA: (aciertos / total_preguntas) * 100
    """
    if total_preguntas <= 0:
        return 0.0
    porcentaje = (aciertos / total_preguntas) * 100.0
    return round(porcentaje, 1)


def calcular_ranking(historial):
    """
    QUÉ HACE: Toma la lista completa de partidas registradas, agrupa los resultados
    por cada jugador y calcula sus estadísticas acumuladas utilizando 'statistics.mean'.
    POR QUÉ: Genera la tabla de posiciones clasificada de mejor a peor puntaje.

    RETORNA:
        Una lista de diccionarios ordenada por el mejor puntaje (y promedio) de cada jugador.
    """
    if not historial:
        return []

    # Diccionario temporal para agrupar partidas por nombre de jugador
    jugadores = {}

    for partida in historial:
        nombre = partida.get("jugador", "Anónimo").strip()
        puntaje = partida.get("puntaje", 0)
        efectividad = partida.get("efectividad", 0.0)

        if nombre not in jugadores:
            jugadores[nombre] = {
                "puntajes": [],
                "efectividades": []
            }

        jugadores[nombre]["puntajes"].append(puntaje)
        jugadores[nombre]["efectividades"].append(efectividad)

    # Ahora procesamos las métricas individuales de cada jugador usando 'statistics'
    ranking = []
    for nombre, datos in jugadores.items():
        lista_pts = datos["puntajes"]
        lista_efect = datos["efectividades"]

        # Usamos statistics.mean() para calcular el promedio de puntaje y de efectividad
        promedio_pts = round(statistics.mean(lista_pts), 1)
        promedio_efect = round(statistics.mean(lista_efect), 1)
        mejor_pts = max(lista_pts)
        total_partidas = len(lista_pts)

        ranking.append({
            "jugador": nombre,
            "partidas": total_partidas,
            "mejor_puntaje": mejor_pts,
            "puntaje_promedio": promedio_pts,
            "efectividad_promedio": promedio_efect
        })

    # Ordenamos el ranking: primero por mejor puntaje descendente, luego por promedio
    ranking.sort(key=lambda x: (x["mejor_puntaje"], x["puntaje_promedio"]), reverse=True)

    return ranking


def calcular_metricas_generales(historial):
    """
    QUÉ HACE: Calcula estadísticas globales de todo el sistema sobre todas las partidas jugadas.
    POR QUÉ: Permite responder preguntas globales como: ¿cuál es el promedio general de puntos?,
    ¿cuál es la categoría más popular?, ¿cuántos usuarios distintos han jugado?

    RETORNA:
        Un diccionario con indicadores globales calculados con 'statistics'.
    """
    if not historial:
        return {
            "total_partidas": 0,
            "total_jugadores": 0,
            "record_puntaje": 0,
            "jugador_record": "-",
            "promedio_global_puntos": 0.0,
            "efectividad_promedio_global": 0.0,
            "categoria_favorita": "-"
        }

    total_partidas = len(historial)
    todos_puntajes = [p.get("puntaje", 0) for p in historial]
    todas_efectividades = [p.get("efectividad", 0.0) for p in historial]
    todas_categorias = [p.get("categoria", "Mixto") for p in historial]
    jugadores_unicos = {p.get("jugador", "Anónimo").strip() for p in historial}

    # Calculamos el promedio global de puntos y efectividad usando statistics.mean
    promedio_global_pts = round(statistics.mean(todos_puntajes), 1)
    promedio_global_efect = round(statistics.mean(todas_efectividades), 1)

    # Obtenemos la partida récord
    record_pts = max(todos_puntajes)
    partida_record = next((p for p in historial if p.get("puntaje", 0) == record_pts), None)
    jugador_record = partida_record.get("jugador", "-") if partida_record else "-"

    # Determinamos la categoría más jugada usando statistics.mode()
    # Si hay empate múltiple, capturamos StatisticsError de forma segura
    try:
        categoria_favorita = statistics.mode(todas_categorias)
    except statistics.StatisticsError:
        # En caso de empate en frecuencia, tomamos la primera
        categoria_favorita = todas_categorias[0] if todas_categorias else "-"

    return {
        "total_partidas": total_partidas,
        "total_jugadores": len(jugadores_unicos),
        "record_puntaje": record_pts,
        "jugador_record": jugador_record,
        "promedio_global_puntos": promedio_global_pts,
        "efectividad_promedio_global": promedio_global_efect,
        "categoria_favorita": categoria_favorita
    }
