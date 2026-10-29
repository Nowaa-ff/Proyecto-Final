# 📖 GUÍA COMPLETA PARA TU EXPOSICIÓN ORAL
## Proyecto: Trivia App & Ranking Manager

Este documento está diseñado especialmente para que estudies y prepares tu defensa oral de **5 minutos**. Contiene una explicación sencilla de cada archivo y bloque de código, además de las preguntas más habituales que un profesor de secundaria suele hacer en estas evaluaciones.

---

## ⏱️ Estructura recomendada para tu exposición (5 minutos)

| Tiempo | Qué decir o mostrar |
|---|---|
| **Minuto 1:00** | **Introducción:** Saludo, nombre del proyecto ("Trivia App & Ranking Manager"), problema que resuelve y por qué decidiste programarlo en Python con arquitectura modular. |
| **Minuto 2:00** | **Demostración en vivo:** Ejecutas `python main.py`. Ingresas tu nombre, seleccionas una categoría (ej. Deportes o Ciencia), respondes un par de preguntas rápido (mostrando el bono verde) y una lento (mostrando el aviso amarillo). Muestras la barra de progreso. |
| **Minuto 3:00** | **Ranking y Estadísticas:** Muestras la tabla de posiciones en consola con medallas, explicas cómo se usó la biblioteca oficial `statistics` para promedios y efectividad. |
| **Minuto 4:00** | **Exportación a Excel:** Seleccionas la opción 3, abres el archivo `reporte_trivia.xlsx` generado por `openpyxl` y muestras las dos hojas ("Ranking" e "Historial") con sus encabezados con color y columnas autoajustadas. |
| **Minuto 5:00** | **Conclusión y preguntas:** Cierras destacando las bibliotecas empleadas (`rich`, `openpyxl`, `statistics`, `json`, `time`) y quedas a disposición del profesor. |

---

## 🔍 Resumen archivo por archivo y bloques de código

### 1. `main.py` (El director de orquesta)
- **¿Qué es?**: Es el punto de partida del programa. Es el archivo que ejecutamos con `python main.py`.
- **Bloques principales**:
  - `main()`: Contiene un bucle `while True` que mantiene el menú abierto hasta que el usuario elija la opción 4 ("Salir").
  - `ver_ranking_y_estadisticas()`: Carga los datos del historial, llama a las funciones matemáticas de `estadisticas.py` y le pide a `interfaz.py` que dibuje las tablas.
  - `exportar_reporte()`: Llama a `exportar.py` para generar el archivo Excel y muestra un mensaje de éxito en verde.
  - `try / except KeyboardInterrupt`: Permite que si alguien presiona `Ctrl+C` en la terminal, el juego se despida educadamente en lugar de mostrar un error rojo del sistema.

### 2. `interfaz.py` (La cara visual del juego)
- **¿Qué es?**: Centraliza todos los textos, colores, paneles y tablas para que la consola parezca una aplicación moderna en lugar de una terminal aburrida.
- **¿Por qué usamos `rich`?**: Porque permite crear tablas con bordes redondeados (`box.ROUNDED`), paneles (`Panel`) y colores sin tener que instalar entornos gráficos pesados.
- **Bloques principales**:
  - `consola = Console()`: Crea la herramienta de Rich que dibuja todo con estilos.
  - `mostrar_banner()` y `mostrar_menu_principal()`: Muestran los títulos y opciones principales.
  - `dibujar_barra_progreso(actual, total)`: Calcula cuántos caracteres pintar (ej. `[████░░░░░░] 40%`) para mostrar visualmente el avance del jugador.
  - `mostrar_pregunta(...)`: Imprime la tarjeta con la pregunta y las 4 opciones numeradas.
  - `mostrar_resultado_respuesta(...)`:
    - **Verde**: Si acertó en menos de 15 segundos.
    - **Amarillo**: Si acertó pero tardó más de 15 segundos (penalizado).
    - **Rojo**: Si falló la pregunta, indicándole cuál era la correcta.
  - `mostrar_tabla_ranking(...)` y `mostrar_tabla_historial(...)`: Construyen tablas con columnas ordenadas y medallas de podio (🥇, 🥈, 🥉).

### 3. `juego.py` (El cerebro y las reglas de la partida)
- **¿Qué es?**: Controla la partida: carga preguntas, mide el tiempo y calcula el puntaje.
- **¿Por qué usamos `time`?**: Con `time.time()` guardamos la hora exacta en segundos antes de que el jugador lea la pregunta, y volvemos a llamar a `time.time()` cuando presiona Enter. Restando ambos tiempos sabemos cuántos segundos tardó con precisión decimal.
- **¿Por qué usamos `random.sample`?**: Para elegir preguntas al azar sin que se repitan dentro de la misma partida.
- **Bloques principales**:
  - `cargar_preguntas()`: Abre `datos/preguntas.json` y maneja errores si el archivo no existe o está dañado.
  - `cargar_historial()` y `guardar_partida()`: Gestionan el archivo `datos/usuarios.json`. Si no existe, lo crean automáticamente como una lista vacía `[]`.
  - `calcular_puntos_pregunta(...)`:
    - Si falla: 0 puntos.
    - Si acierta en $\le 15$ segundos: 100 puntos base + 10 puntos por cada segundo sobrante.
    - Si acierta en $> 15$ segundos: 100 puntos base menos penalización por lentitud (garantizando al menos 30 puntos por acierto).
  - `iniciar_partida()`: El bucle que recorre las preguntas una a una, cronometra y al final calcula el tiempo promedio y la efectividad.

### 4. `estadisticas.py` (Los cálculos matemáticos)
- **¿Qué es?**: Se encarga de procesar los números del juego.
- **¿Por qué usamos `statistics`?**: Es la biblioteca matemática oficial de Python. Proporciona funciones probadas y confiables como `mean()` (media aritmética o promedio) y `mode()` (moda o valor más frecuente).
- **Bloques principales**:
  - `calcular_efectividad(aciertos, total)`: Calcula el porcentaje mediante la fórmula: `(aciertos / total) * 100`.
  - `calcular_ranking(historial)`: Agrupa todas las partidas por el nombre del jugador, calcula su puntaje promedio y efectividad promedio con `statistics.mean`, y los ordena de mayor a menor según su mejor partida.
  - `calcular_metricas_generales(historial)`: Calcula el récord histórico, el total de jugadores únicos y la categoría favorita con `statistics.mode`.

### 5. `exportar.py` (El generador de Excel)
- **¿Qué es?**: Crea el archivo `reporte_trivia.xlsx` con dos pestañas u hojas de cálculo.
- **¿Por qué usamos `openpyxl`?**: Es la biblioteca estándar para crear archivos nativos de Excel desde Python.
- **Bloques principales**:
  - `wb = openpyxl.Workbook()`: Crea un archivo de Excel vacío en memoria.
  - `ws_ranking = wb.active` / `ws_historial = wb.create_sheet(...)`: Crea las dos hojas ("Ranking" e "Historial").
  - `aplicar_estilo_encabezado(...)`: Pinta la primera fila con color de fondo (azul institucional), texto blanco en negrita y centrado.
  - `autoajustar_columnas(...)`: Recorre las celdas, mide el texto más largo y ajusta el ancho de cada columna para que nada se corte ni aparezcan signos `###`.
  - `wb.save("reporte_trivia.xlsx")`: Guarda el archivo en el disco. Además, tiene un `try/except PermissionError` por si el usuario tiene el Excel abierto al momento de exportar.

### 6. `datos/preguntas.json` y `datos/usuarios.json`
- **`preguntas.json`**: Contiene 40 preguntas organizadas con sus 4 opciones, el número de opción correcta (del 1 al 4) y su categoría.
- **`usuarios.json`**: Es la base de datos local en formato JSON donde se agregan automáticamente las partidas con fecha y hora (`datetime.now()`).

---

## ❓ 5 Preguntas típicas que te puede hacer el profesor (con respuestas preparadas)

### Pregunta 1: *"¿Por qué dividiste el código en varios archivos (.py) en lugar de hacer todo en un solo script?"*
> **Tu respuesta:**  
> *"Lo dividí en varios módulos para aplicar el principio de **separación de responsabilidades** (buenas prácticas de ingeniería de software). De esta manera:*
> - *`interfaz.py` solo se ocupa de lo visual.*
> - *`juego.py` maneja las reglas del juego.*
> - *`estadisticas.py` se enfoca en los cálculos.*
> - *`exportar.py` se encarga del archivo Excel.*
> - *Y `main.py` actúa como menú central.*  
> *Esto hace que el código sea mucho más fácil de leer, mantener y corregir sin que un cambio en la interfaz afecte la lógica matemática."*

---

### Pregunta 2: *"¿Cómo mediste el tiempo de respuesta del usuario sin cortar el programa bruscamente?"*
> **Tu respuesta:**  
> *"Utilicé el módulo estándar `time` guardando una marca de tiempo con `time.time()` justo antes de mostrar el `input()`, y otra marca inmediatamente después de que el usuario presiona Enter.  
> La diferencia `tiempo_fin - tiempo_inicio` me da los segundos exactos con decimales. Si tardó menos de 15 segundos le otorgamos un bono de velocidad, y si superó los 15 segundos le aplicamos una penalización de puntos. Así no necesitamos cortar la consola a la fuerza y la experiencia de juego es fluida."*

---

### Pregunta 3: *"¿Qué pasa si el archivo `usuarios.json` no existe en la computadora cuando se ejecuta el programa por primera vez?"*
> **Tu respuesta:**  
> *"El programa está programado para ser tolerante a fallos: la función `cargar_historial()` verifica con `os.path.exists()` si el archivo existe. Si no existe, crea automáticamente la carpeta y un archivo `usuarios.json` inicializado con una lista vacía `[]`. De este modo, la aplicación nunca se rompe ni lanza un error en la primera ejecución."*

---

### Pregunta 4: *"¿Para qué usaste el módulo `statistics` y no un simple cálculo manual?"*
> **Tu respuesta:**  
> *"Utilicé el módulo oficial `statistics` de la biblioteca estándar de Python (específicamente `statistics.mean` y `statistics.mode`) porque es una biblioteca optimizada, legible y robusta. En lugar de escribir fórmulas repetitivas con bucles y divisiones manuales, `statistics.mean(lista)` calcula el promedio de puntaje y de efectividad de cada jugador de forma limpia y profesional."*

---

### Pregunta 5: *"¿Qué cuidados tuviste al generar el archivo Excel con `openpyxl`?"*
> **Tu respuesta:**  
> *"Principalmente dos aspectos:*
> 1. ***Diseño y legibilidad:** No solo inserté los datos en crudo, sino que apliqué formato con `PatternFill` y `Font` para que los encabezados tengan fondo azul y texto blanco en negrita, y programé una función que autoajusta el ancho de cada columna según la longitud de su texto.*
> 2. ***Manejo de excepciones:** Capturé el error `PermissionError`, que ocurre muy comúnmente cuando el usuario intenta exportar mientras tiene el archivo Excel abierto en su computadora. El programa le avisa amablemente en pantalla que debe cerrar el archivo antes de continuar en lugar de crashear."*
