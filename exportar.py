"""
==============================================================================
MÓDULO DE EXPORTACIÓN A EXCEL (exportar.py)
==============================================================================
Este archivo genera un archivo de hoja de cálculo (.xlsx) profesional
utilizando la biblioteca externa 'openpyxl'.

¿POR QUÉ SE USA OPENPYXL?
openpyxl es la biblioteca estándar de facto en Python para crear, leer y editar
archivos Excel modernos (.xlsx). Permite dar formato a celdas, colores de fondo,
fuentes en negrita, bordes y ajustar automáticamente el ancho de columnas,
creando reportes presentables para empresas o instituciones escolares.
==============================================================================
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from estadisticas import calcular_ranking


def aplicar_estilo_encabezado(hoja, columnas, color_fondo="1F4E79"):
    """
    QUÉ HACE: Aplica estilo profesional a la primera fila (los encabezados).
    POR QUÉ: Mejora la legibilidad del reporte en Excel con texto blanco en negrita,
    fondo de color institucional y centrado vertical y horizontal.
    """
    fuente_blanca_negrita = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    relleno_encabezado = PatternFill(start_color=color_fondo, end_color=color_fondo, fill_type="solid")
    alineacion_centrada = Alignment(horizontal="center", vertical="center", wrap_text=True)

    borde_fino = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="medium", color="000000")
    )

    hoja.row_dimensions[1].height = 28

    for num_col in range(1, len(columnas) + 1):
        celda = hoja.cell(row=1, column=num_col)
        celda.font = fuente_blanca_negrita
        celda.fill = relleno_encabezado
        celda.alignment = alineacion_centrada
        celda.border = borde_fino


def autoajustar_columnas(hoja):
    """
    QUÉ HACE: Recorre cada columna y ajusta su ancho al tamaño del texto más largo.
    POR QUÉ: Evita que los textos queden recortados o aparezcan los molestos '###' en Excel.
    """
    borde_celda = Border(
        left=Side(style="thin", color="E0E0E0"),
        right=Side(style="thin", color="E0E0E0"),
        top=Side(style="thin", color="E0E0E0"),
        bottom=Side(style="thin", color="E0E0E0")
    )

    for col in hoja.columns:
        longitud_maxima = 0
        col_letra = get_column_letter(col[0].column)

        for celda in col:
            # Aplicamos bordes a todas las celdas de datos para que se vea como tabla
            if celda.row > 1:
                celda.border = borde_celda

            if celda.value is not None:
                longitud_maxima = max(longitud_maxima, len(str(celda.value)))

        # Le damos un margen extra de 4 caracteres, con mínimo de 14
        hoja.column_dimensions[col_letra].width = max(longitud_maxima + 4, 14)


def exportar_reporte_excel(historial, ruta_archivo="reporte_trivia.xlsx"):
    """
    QUÉ HACE: Crea un libro de Excel con dos hojas:
    1. 'Ranking': Tabla de posiciones consolidada de jugadores.
    2. 'Historial': Registro detallado de cada partida jugada con fecha, hora y puntaje.
    POR QUÉ: Permite exportar y compartir los datos del juego de forma ordenada
    y compatible con Microsoft Excel, Google Sheets o LibreOffice.

    RETORNA:
        (bool, str): Tupla con True si tuvo éxito o False si hubo un error, más un mensaje.
    """
    if not historial:
        return False, "No hay partidas en el historial para exportar."

    try:
        # Creamos un nuevo libro de trabajo de openpyxl
        wb = openpyxl.Workbook()

        # ====================================================================
        # HOJA 1: RANKING
        # ====================================================================
        ws_ranking = wb.active
        ws_ranking.title = "Ranking"

        encabezados_ranking = [
            "Posición",
            "Jugador",
            "Partidas Jugadas",
            "Mejor Puntaje",
            "Puntaje Promedio",
            "Efectividad Promedio (%)"
        ]
        ws_ranking.append(encabezados_ranking)

        # Calculamos la tabla de ranking agrupada
        lista_ranking = calcular_ranking(historial)

        alineacion_centro = Alignment(horizontal="center", vertical="center")
        alineacion_izq = Alignment(horizontal="left", vertical="center")

        for pos, fila in enumerate(lista_ranking, start=1):
            ws_ranking.append([
                f"{pos}°",
                fila["jugador"],
                fila["partidas"],
                fila["mejor_puntaje"],
                fila["puntaje_promedio"],
                f"{fila['efectividad_promedio']}%"
            ])
            # Alineamos las celdas de la fila recién agregada
            fila_actual = ws_ranking.max_row
            ws_ranking.cell(row=fila_actual, column=1).alignment = alineacion_centro
            ws_ranking.cell(row=fila_actual, column=2).alignment = alineacion_izq
            for c in range(3, 7):
                ws_ranking.cell(row=fila_actual, column=c).alignment = alineacion_centro

        # Aplicamos estilo azul institucional al encabezado de Ranking
        aplicar_estilo_encabezado(ws_ranking, encabezados_ranking, color_fondo="1F4E79")
        autoajustar_columnas(ws_ranking)

        # ====================================================================
        # HOJA 2: HISTORIAL
        # ====================================================================
        ws_historial = wb.create_sheet(title="Historial")

        encabezados_historial = [
            "N° Partida",
            "Fecha y Hora",
            "Jugador",
            "Categoría",
            "Puntaje Obtenido",
            "Aciertos",
            "Total Preguntas",
            "Efectividad (%)",
            "Tiempo Promedio (s)"
        ]
        ws_historial.append(encabezados_historial)

        for i, p in enumerate(historial, start=1):
            ws_historial.append([
                i,
                p.get("fecha", "-"),
                p.get("jugador", "-"),
                p.get("categoria", "-"),
                p.get("puntaje", 0),
                p.get("aciertos", 0),
                p.get("total_preguntas", 0),
                f"{p.get('efectividad', 0.0):.1f}%",
                f"{p.get('tiempo_promedio', 0.0):.1f} s"
            ])
            fila_actual = ws_historial.max_row
            ws_historial.cell(row=fila_actual, column=1).alignment = alineacion_centro
            ws_historial.cell(row=fila_actual, column=2).alignment = alineacion_centro
            ws_historial.cell(row=fila_actual, column=3).alignment = alineacion_izq
            for c in range(4, 10):
                ws_historial.cell(row=fila_actual, column=c).alignment = alineacion_centro

        # Aplicamos estilo verde elegante al encabezado de Historial
        aplicar_estilo_encabezado(ws_historial, encabezados_historial, color_fondo="2E75B6")
        autoajustar_columnas(ws_historial)

        # Guardamos el archivo en disco
        wb.save(ruta_archivo)
        ruta_absoluta = os.path.abspath(ruta_archivo)
        return True, f"Reporte exportado exitosamente en:\n{ruta_absoluta}"

    except PermissionError:
        # Error clásico: el usuario tiene el archivo abierto en Excel y el sistema no deja sobreescribirlo
        return False, (
            f"No se pudo escribir en '{ruta_archivo}' porque el archivo está abierto en Excel u otro programa.\n"
            f"Por favor, cierra el archivo y vuelve a intentar."
        )
    except Exception as e:
        return False, f"Ocurrió un error inesperado al exportar: {str(e)}"
