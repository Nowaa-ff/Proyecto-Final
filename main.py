"""
==============================================================================
ARCHIVO PRINCIPAL (main.py)
==============================================================================
Proyecto: Trivia App & Ranking Manager
Autor: Estudiante de Secundaria - Proyecto Final de Programación
Descripción: Menú principal interactivo que conecta todos los módulos:
             - juego.py: Partida y cronómetro
             - estadisticas.py: Cálculos con módulo statistics
             - exportar.py: Reportes en Excel con openpyxl
             - interfaz.py: Diseño visual de consola con rich

¿POR QUÉ ESTÁ ESTRUCTURADO ASÍ?
Tener un archivo 'main.py' como punto de entrada único sigue las buenas
prácticas de programación modular: cada archivo se encarga de una tarea
específica (separación de responsabilidades), haciendo que el código sea
fácil de leer, corregir y explicar en una exposición oral.
==============================================================================
"""

import sys

# Aseguramos compatibilidad total con UTF-8 en terminales de Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import interfaz
import juego
import estadisticas
import exportar


def ver_ranking_y_estadisticas():
    """
    QUÉ HACE: Carga el historial de partidas, procesa las métricas usando
    el módulo 'estadisticas' y muestra las tablas y paneles en pantalla.
    POR QUÉ: Permite a los jugadores ver el salón de la fama y las estadísticas generales.
    """
    interfaz.limpiar_pantalla()
    interfaz.mostrar_banner()

    historial = juego.cargar_historial()

    if not historial:
        interfaz.mostrar_mensaje_aviso(
            "Todavía no se ha jugado ninguna partida.\n"
            "¡Juega una partida desde el Menú Principal para estrenar el ranking!"
        )
        interfaz.pausar()
        return

    # 1. Calculamos el ranking de mejores jugadores
    ranking = estadisticas.calcular_ranking(historial)

    # 2. Calculamos las métricas globales con el módulo 'statistics'
    metricas = estadisticas.calcular_metricas_generales(historial)

    # 3. Mostramos las tablas visuales con Rich
    interfaz.mostrar_tabla_ranking(ranking)
    interfaz.mostrar_panel_estadisticas_generales(metricas)
    interfaz.mostrar_tabla_historial(historial, limite=8)

    interfaz.pausar()


def exportar_reporte():
    """
    QUÉ HACE: Solicita la exportación a un archivo Excel (.xlsx) con dos hojas.
    POR QUÉ: Permite al usuario generar un reporte descargable para abrirlo en Excel.
    """
    interfaz.limpiar_pantalla()
    interfaz.mostrar_banner()

    historial = juego.cargar_historial()

    if not historial:
        interfaz.mostrar_mensaje_aviso(
            "No hay partidas registradas en el sistema para exportar.\n"
            "Juega al menos una partida antes de generar el reporte."
        )
        interfaz.pausar()
        return

    interfaz.consola.print("[bold yellow]Generando archivo Excel con openpyxl...[/bold yellow]")

    import os
    ruta_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reporte_trivia.xlsx")

    # Llamamos a la función de exportación de exportar.py
    exito, mensaje = exportar.exportar_reporte_excel(historial, ruta_archivo=ruta_excel)

    if exito:
        interfaz.mostrar_mensaje_exito(mensaje)
    else:
        interfaz.mostrar_mensaje_error(mensaje)

    interfaz.pausar()


def main():
    """
    QUÉ HACE: Función principal que contiene el bucle infinito del menú interactivo.
    POR QUÉ: Mantiene el programa en ejecución hasta que el usuario decida salir explícitamente.
    """
    while True:
        try:
            interfaz.limpiar_pantalla()
            interfaz.mostrar_banner()
            interfaz.mostrar_menu_principal()

            interfaz.consola.print("[bold yellow]Selecciona una opción (1-4):[/bold yellow] ", end="")
            opcion = input().strip()

            if opcion == "1":
                # Iniciar una partida interactiva de trivia
                juego.iniciar_partida()

            elif opcion == "2":
                # Ver ranking de jugadores y estadísticas
                ver_ranking_y_estadisticas()

            elif opcion == "3":
                # Exportar datos a Microsoft Excel
                exportar_reporte()

            elif opcion == "4":
                # Salir del juego
                interfaz.limpiar_pantalla()
                interfaz.consola.print(
                    "\n[bold green]👋 ¡Muchas gracias por jugar a Trivia App & Ranking Manager![/bold green]\n"
                    "[dim]¡Éxitos en tu exposición escolar![/dim]\n"
                )
                break

            else:
                interfaz.mostrar_mensaje_error("Opción inválida. Por favor, ingresa un número del 1 al 4.")
                interfaz.pausar()

        except (KeyboardInterrupt, EOFError):
            # Captura Ctrl+C o fin de archivo (EOF) para salir limpiamente
            interfaz.consola.print("\n\n[bold yellow]Programa finalizado. ¡Hasta pronto![/bold yellow]\n")
            break
        except Exception as e:
            # Captura cualquier error imprevisto para que la aplicación no se cierre de golpe
            interfaz.mostrar_mensaje_error(f"Ocurrió un error inesperado: {str(e)}")
            interfaz.pausar()


if __name__ == "__main__":
    main()
