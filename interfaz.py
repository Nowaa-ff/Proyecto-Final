"""
==============================================================================
MÓDULO DE INTERFAZ GRÁFICA DE CONSOLA (interfaz.py)
==============================================================================
Este archivo centraliza todo el aspecto visual del programa utilizando
la biblioteca externa 'rich'.

¿POR QUÉ SE USA RICH?
Rich permite dar estilo profesional a la consola mediante colores, tablas,
paneles y bordes sin necesidad de crear una interfaz gráfica pesada (como Tkinter),
manteniendo el código simple, moderno y compatible con cualquier terminal.
==============================================================================
"""

import os
import sys

# Aseguramos compatibilidad total con UTF-8 en terminales de Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# Creamos una única instancia global de la consola de Rich para todo el proyecto.
# Esto asegura que todos los módulos compartan el mismo formateador visual.
consola = Console()


def limpiar_pantalla():
    """
    QUÉ HACE: Limpia la pantalla de la terminal.
    POR QUÉ: Para que cada menú o pregunta se vea limpio y ordenado,
    evitando que la pantalla se llene de texto viejo acumulado.
    """
    consola.clear()


def pausar():
    """
    QUÉ HACE: Espera a que el usuario presione la tecla ENTER.
    POR QUÉ: Permite al jugador leer tablas, estadísticas o resultados
    antes de que la pantalla se limpie y regrese al menú principal.
    """
    consola.print("\n[bold dim cyan]Presiona [white]ENTER[/white] para continuar...[/bold dim cyan]", end="")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass


def mostrar_banner():
    """
    QUÉ HACE: Muestra el título principal y bienvenida del juego.
    POR QUÉ: Da una presentación atractiva al inicio del programa
    y en el menú principal.
    """
    texto_titulo = (
        "[bold cyan]🧠 TRIVIA APP & RANKING MANAGER 🏆[/bold cyan]\n"
        "[italic bright_white]Demuestra tus conocimientos, compite por el podio y genera tus reportes[/italic bright_white]"
    )
    banner = Panel(
        texto_titulo,
        box=box.DOUBLE_EDGE,
        border_style="bold blue",
        expand=False,
        padding=(1, 4)
    )
    consola.print(banner, justify="center")


def mostrar_menu_principal():
    """
    QUÉ HACE: Despliega las 4 opciones principales del juego con estilo.
    POR QUÉ: Ofrece una navegación clara e intuitiva para el usuario.
    """
    menu_texto = (
        "[bold green]1.[/bold green] 🎮 [bold white]Jugar partida de trivia[/bold white]\n"
        "[bold yellow]2.[/bold yellow] 📊 [bold white]Ver ranking y estadísticas[/bold white]\n"
        "[bold cyan]3.[/bold cyan] 📁 [bold white]Exportar reporte a Excel (.xlsx)[/bold white]\n"
        "[bold red]4.[/bold red] 🚪 [bold white]Salir del programa[/bold white]"
    )
    panel_menu = Panel(
        menu_texto,
        title="[bold yellow]Menú Principal[/bold yellow]",
        title_align="left",
        border_style="bright_blue",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    consola.print(panel_menu)


def mostrar_menu_categorias():
    """
    QUÉ HACE: Presenta la lista de categorías disponibles para jugar.
    POR QUÉ: El usuario debe poder elegir el tema que más le guste o elegir 'Mixto'.
    """
    texto = (
        "[bold cyan]1.[/bold cyan] 🌍 Cultura General\n"
        "[bold cyan]2.[/bold cyan] 🔬 Ciencia\n"
        "[bold cyan]3.[/bold cyan] 📜 Historia\n"
        "[bold cyan]4.[/bold cyan] ⚽ Deportes\n"
        "[bold cyan]5.[/bold cyan] 🎲 Mixto (Preguntas variadas al azar)"
    )
    panel = Panel(
        texto,
        title="[bold green]Selecciona una Categoría[/bold green]",
        title_align="left",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    consola.print(panel)


def dibujar_barra_progreso(actual, total, longitud=20):
    """
    QUÉ HACE: Genera una representación visual en texto de una barra de progreso.
    POR QUÉ: Cumple con el requisito de barra de progreso durante la partida
    mostrando visualmente el avance (ej. [████░░░░░░] 40%).
    """
    porcentaje = int((actual / total) * 100) if total > 0 else 0
    bloques_llenos = int((actual / total) * longitud) if total > 0 else 0
    bloques_vacios = longitud - bloques_llenos
    barra = "█" * bloques_llenos + "░" * bloques_vacios
    return f"[bold cyan][{barra}][/bold cyan] [bold yellow]{actual}/{total}[/bold yellow] ({porcentaje}%)"


def mostrar_pregunta(numero_actual, total_preguntas, datos_pregunta):
    """
    QUÉ HACE: Muestra el panel con la pregunta actual, su categoría,
    la barra de progreso de la partida y las cuatro opciones numeradas.
    POR QUÉ: Proporciona al jugador toda la información necesaria
    para responder de forma visualmente atractiva y cómoda.
    """
    categoria = datos_pregunta.get("categoria", "General")
    pregunta_texto = datos_pregunta.get("pregunta", "")
    opciones = datos_pregunta.get("opciones", [])

    # Construimos el texto con las 4 opciones
    texto_opciones = "\n".join([
        f"  [bold yellow][{i + 1}][/bold yellow] [white]{opcion}[/white]"
        for i, opcion in enumerate(opciones)
    ])

    barra_progreso = dibujar_barra_progreso(numero_actual, total_preguntas)

    contenido = (
        f"Progreso: {barra_progreso}\n"
        f"Categoría: [bold magenta]{categoria}[/bold magenta]\n\n"
        f"[bold white]{pregunta_texto}[/bold white]\n\n"
        f"[bold underline]Opciones:[/bold underline]\n{texto_opciones}\n\n"
        f"[dim]⏱️  Tiempo límite sugerido: 15 segundos (¡responde rápido para bonificar!)[/dim]"
    )

    panel = Panel(
        contenido,
        title=f"[bold bright_blue]Pregunta #{numero_actual} de {total_preguntas}[/bold bright_blue]",
        title_align="left",
        border_style="bright_blue",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    consola.print(panel)


def mostrar_resultado_respuesta(es_correcta, tiempo_segundos, puntos, penalizado, texto_correcta):
    """
    QUÉ HACE: Informa inmediatamente si la respuesta fue correcta o no,
    con colores específicos según el enunciado:
    - Verde: Respuesta correcta en tiempo óptimo.
    - Amarillo: Respuesta correcta pero con tiempo excedido (> 15 s).
    - Rojo: Respuesta incorrecta.
    POR QUÉ: Da retroalimentación instantánea al jugador sobre su desempeño.
    """
    if es_correcta and not penalizado:
        # Estado Verde: acierto rápido
        mensaje = (
            f"🎉 [bold green]¡RESPUESTA CORRECTA![/bold green]\n"
            f"⏱️  Tiempo: [bold white]{tiempo_segundos:.1f} s[/bold white] (¡Excelente velocidad!)\n"
            f"⭐ Puntos sumados: [bold green]+{puntos}[/bold green]"
        )
        panel = Panel(mensaje, border_style="bold green", box=box.ROUNDED)
        consola.print(panel)

    elif es_correcta and penalizado:
        # Estado Amarillo: acierto pero tardó más de 15 segundos
        mensaje = (
            f"⚠️ [bold yellow]¡CORRECTA, PERO CON TIEMPO EXCEDIDO![/bold yellow]\n"
            f"⏱️  Tiempo: [bold white]{tiempo_segundos:.1f} s[/bold white] (Límite: 15 s)\n"
            f"⭐ Puntos sumados: [bold yellow]+{puntos}[/bold yellow] [dim](penalización aplicada por demora)[/dim]"
        )
        panel = Panel(mensaje, border_style="bold yellow", box=box.ROUNDED)
        consola.print(panel)

    else:
        # Estado Rojo: respuesta incorrecta
        mensaje = (
            f"❌ [bold red]¡RESPUESTA INCORRECTA![/bold red]\n"
            f"⏱️  Tiempo: [bold white]{tiempo_segundos:.1f} s[/bold white]\n"
            f"⭐ Puntos sumados: [bold red]+0[/bold red]\n"
            f"💡 La opción correcta era: [bold cyan]{texto_correcta}[/bold cyan]"
        )
        panel = Panel(mensaje, border_style="bold red", box=box.ROUNDED)
        consola.print(panel)


def mostrar_resumen_partida(jugador, categoria, puntaje, aciertos, total, efectividad, tiempo_promedio):
    """
    QUÉ HACE: Despliega una tarjeta resumen al terminar la partida con todas las estadísticas.
    POR QUÉ: El jugador necesita ver su balance final de puntaje y aciertos obtenidos.
    """
    resumen = (
        f"👤 [bold white]Jugador:[/bold white] [bold cyan]{jugador}[/bold cyan]\n"
        f"🏷️  [bold white]Categoría:[/bold white] [magenta]{categoria}[/magenta]\n"
        f"🏆 [bold white]Puntaje Total:[/bold white] [bold green]{puntaje} pts[/bold green]\n"
        f"🎯 [bold white]Aciertos:[/bold white] {aciertos} de {total} preguntas\n"
        f"📈 [bold white]Efectividad:[/bold white] [bold yellow]{efectividad:.1f}%[/bold yellow]\n"
        f"⏱️  [bold white]Tiempo promedio por respuesta:[/bold white] {tiempo_promedio:.1f} s"
    )
    panel = Panel(
        resumen,
        title="[bold yellow]🎉 ¡Partida Finalizada! - Resumen de Desempeño 🎉[/bold yellow]",
        border_style="yellow",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )
    consola.print(panel)


def mostrar_tabla_ranking(lista_ranking):
    """
    QUÉ HACE: Dibuja una tabla elegante con las mejores posiciones de jugadores.
    POR QUÉ: Permite visualizar de forma ordenada el salón de la fama del juego.
    """
    if not lista_ranking:
        mostrar_mensaje_aviso("No hay jugadores en el ranking todavía. ¡Sé el primero en jugar!")
        return

    tabla = Table(
        title="🏆 TABLA DE POSICIONES GENERAL 🏆",
        box=box.ROUNDED,
        header_style="bold bright_cyan",
        border_style="bright_blue"
    )

    tabla.add_column("Pos.", justify="center", style="bold yellow")
    tabla.add_column("Jugador", justify="left", style="bold white")
    tabla.add_column("Partidas", justify="center")
    tabla.add_column("Mejor Puntaje", justify="center", style="bold green")
    tabla.add_column("Puntaje Promedio", justify="center", style="cyan")
    tabla.add_column("Efectividad Media", justify="center", style="bold magenta")

    # Íconos para los 3 primeros lugares
    medallas = {1: "🥇 1°", 2: "🥈 2°", 3: "🥉 3°"}

    for i, fila in enumerate(lista_ranking, start=1):
        pos_texto = medallas.get(i, f"{i}°")
        tabla.add_row(
            pos_texto,
            str(fila["jugador"]),
            str(fila["partidas"]),
            str(fila["mejor_puntaje"]),
            f"{fila['puntaje_promedio']:.1f}",
            f"{fila['efectividad_promedio']:.1f}%"
        )

    consola.print(tabla)


def mostrar_tabla_historial(lista_historial, limite=10):
    """
    QUÉ HACE: Dibuja una tabla con el registro cronológico de las partidas más recientes.
    POR QUÉ: Permite a los usuarios consultar el detalle histórico de cada partida jugada.
    """
    if not lista_historial:
        mostrar_mensaje_aviso("El historial de partidas está vacío.")
        return

    tabla = Table(
        title=f"📜 HISTORIAL RECIENTE (Últimas {min(len(lista_historial), limite)} partidas) 📜",
        box=box.ROUNDED,
        header_style="bold bright_white",
        border_style="cyan"
    )

    tabla.add_column("Fecha y Hora", justify="center", style="dim")
    tabla.add_column("Jugador", justify="left", style="bold white")
    tabla.add_column("Categoría", justify="center", style="magenta")
    tabla.add_column("Puntaje", justify="center", style="bold green")
    tabla.add_column("Aciertos", justify="center")
    tabla.add_column("Efectividad", justify="center", style="bold yellow")

    # Mostramos las partidas en orden inverso (las más nuevas primero)
    partidas_recientes = list(reversed(lista_historial))[:limite]

    for p in partidas_recientes:
        tabla.add_row(
            str(p.get("fecha", "-")),
            str(p.get("jugador", "-")),
            str(p.get("categoria", "-")),
            str(p.get("puntaje", 0)),
            f"{p.get('aciertos', 0)}/{p.get('total_preguntas', 0)}",
            f"{p.get('efectividad', 0.0):.1f}%"
        )

    consola.print(tabla)


def mostrar_panel_estadisticas_generales(metricas):
    """
    QUÉ HACE: Muestra un panel con las métricas globales calculadas con el módulo statistics.
    POR QUÉ: Complementa el ranking dando una visión global del uso del juego.
    """
    if not metricas or metricas.get("total_partidas", 0) == 0:
        return

    texto = (
        f"🎮 [bold white]Total de partidas registradas:[/bold white] [bold cyan]{metricas['total_partidas']}[/bold cyan]\n"
        f"👥 [bold white]Jugadores únicos participantes:[/bold white] [bold cyan]{metricas['total_jugadores']}[/bold cyan]\n"
        f"⭐ [bold white]Récord histórico de puntaje:[/bold white] [bold green]{metricas['record_puntaje']} pts[/bold green] "
        f"[dim](por {metricas.get('jugador_record', '-')})[/dim]\n"
        f"📊 [bold white]Puntaje promedio global:[/bold white] [yellow]{metricas['promedio_global_puntos']:.1f} pts[/yellow]\n"
        f"🎯 [bold white]Efectividad promedio global:[/bold white] [magenta]{metricas['efectividad_promedio_global']:.1f}%[/magenta]\n"
        f"🔥 [bold white]Categoría más jugada:[/bold white] [bold bright_white]{metricas.get('categoria_favorita', '-')}[/bold bright_white]"
    )
    panel = Panel(
        texto,
        title="[bold cyan]📈 Estadísticas Globales del Sistema[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    consola.print(panel)


def mostrar_mensaje_exito(mensaje):
    """Muestra una notificación en verde de éxito."""
    consola.print(f"\n[bold green]✓ ÉXITO:[/bold green] [white]{mensaje}[/white]")


def mostrar_mensaje_error(mensaje):
    """Muestra una notificación en rojo de error."""
    consola.print(f"\n[bold red]✗ ERROR:[/bold red] [white]{mensaje}[/white]")


def mostrar_mensaje_aviso(mensaje):
    """Muestra una notificación en amarillo de advertencia."""
    consola.print(f"\n[bold yellow]! ATENCIÓN:[/bold yellow] [white]{mensaje}[/white]")
