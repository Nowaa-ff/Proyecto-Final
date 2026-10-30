# Trivia App & Ranking Manager 

**Proyecto Final de Programación en Python (Nivel Secundario)**  
*Aplicación de consola interactiva para jugar trivias, gestionar rankings competitivos y exportar reportes estadísticos a Microsoft Excel.*

---

## ¿Para qué sirve?
**Trivia App & Ranking Manager** es un juego educativo de preguntas y respuestas en consola diseñado para evaluar conocimientos en diversas temáticas, cronometrar el tiempo de respuesta de cada jugador, premiar la velocidad y generar automáticamente reportes estadísticos en formato Excel (.xlsx).

El proyecto fue desarrollado con un enfoque modular, simple y claro, utilizando funciones con nombres descriptivos en español y comentarios explicativos en cada bloque de código, facilitando su comprensión y defensa en exposiciones orales escolares.

---

## Funcionalidades Principales

1. **Menú Interactivo y Navegación Guiada**:
   - Menú intuitivo por opciones numeradas (1 al 4) con control de errores para entradas no válidas.
2. **Modo de Juego Dinámico y Categorías**:
   - Selección de categorías temáticas: **Cultura General**, **Ciencia**, **Historia**, **Deportes** o **Mixto**.
   - Preguntas seleccionadas al azar mediante `random.sample()` (garantizando que ninguna pregunta se repita en la misma partida).
   - Cantidad de preguntas configurable (5 preguntas para partida rápida o 10 para partida completa).
3. **Cronómetro y Sistema Inteligente de Puntos**:
   - Cada respuesta es cronometrada con el módulo estándar `time`.
   - **Bono por velocidad**: Si respondes en menos de 15 segundos, recibes 100 puntos base más 10 puntos adicionales por cada segundo restante.
   - **Penalización por lentitud**: Si tardas más de 15 segundos, se aplica un descuento proporcional a la demora (mínimo 30 puntos por acierto).
   - Si la respuesta es incorrecta, suma 0 puntos.
4. **Diseño Visual Profesional con Rich**:
   - Paneles estilizados con bordes redondeados para cada pregunta.
   - Barra de progreso visual que muestra el avance (`Pregunta 3 de 5 (60%)`).
   - Colores de retroalimentación inmediata:
     - 🟢 **Verde**: ¡Respuesta correcta a tiempo!
     - 🟡 **Amarillo**: ¡Respuesta correcta pero con tiempo excedido!
     - 🔴 **Rojo**: ¡Respuesta incorrecta!
5. **Módulo de Estadísticas y Ranking**:
   - Cálculo automático de **porcentaje de efectividad** `(aciertos / total) * 100`.
   - Cálculo de **promedio de puntos** y efectividad con el módulo oficial `statistics.mean`.
   - Medición de récords y categoría más jugada con `statistics.mode`.
   - Tabla de posiciones visual con medallas de podio (🥇 1°, 🥈 2°, 🥉 3°).
6. **Exportación de Reportes a Excel (.xlsx)**:
   - Generación de libro Excel profesional con dos hojas formateadas:
     - **Hoja "Ranking"**: Tabla consolidada por jugador con partidas jugadas, mejor puntaje, promedio de puntos y porcentaje de efectividad.
     - **Hoja "Historial"**: Registro detallado de todas las partidas con fecha y hora, jugador, categoría, puntaje, aciertos y efectividad.
   - Encabezados estilizados con colores corporativos, tipografía en negrita blanca, bordes de celdas y autoajuste del ancho de columnas.

---

## Bibliotecas Utilizadas

### Bibliotecas Estándar de Python (No requieren instalación adicional)
- `json`: Manejo de lectura y escritura del banco de preguntas (`preguntas.json`) y la persistencia del historial de partidas (`usuarios.json`).
- `random`: Selección aleatoria y sin repetición de preguntas para cada partida (`random.sample`).
- `time`: Medición precisa del tiempo de respuesta del jugador (`time.time()`).
- `datetime`: Registro de la fecha y hora exacta en la que se disputó cada partida (`datetime.now()`).
- `statistics`: Cálculo matemático riguroso del promedio de puntos (`statistics.mean`), promedio de efectividad y categoría más popular (`statistics.mode`).

### Bibliotecas Externas (Instalables vía pip)
- `rich`: Renderizado en consola de paneles, tablas coloreadas, barras de progreso y estilos visuales modernos.
- `openpyxl`: Creación, diseño de celdas, aplicación de estilos y guardado del archivo de hoja de cálculo `reporte_trivia.xlsx`.

---

## Estructura de Archivos

```text
Proyecto-Final/
├── main.py                 # Punto de entrada principal y bucle del menú
├── juego.py                # Lógica de la partida, cronómetro y cálculo de puntos
├── estadisticas.py         # Métricas matemáticas y ranking (módulo statistics)
├── exportar.py             # Generación y formateo de hojas en Excel (openpyxl)
├── interfaz.py             # Funciones visuales de consola con rich (paneles, tablas, colores)
├── datos/
│   ├── preguntas.json      # Banco con 40 preguntas clasificadas en 4 categorías
│   └── usuarios.json       # Historial persistente de partidas (se crea automáticamente)
├── requirements.txt        # Dependencias externas necesarias (rich, openpyxl)
├── .gitignore              # Archivos ignorados por Git (caché, entornos, .xlsx)
├── EXPLICACION.md          # Guía de estudio y preguntas frecuentes para la exposición oral
└── README.md               # Documentación general del proyecto
```

---

## 💻 Instalación y Ejecución en Windows

### Paso 1: Clonar o descargar el repositorio
Abre una terminal (PowerShell o Símbolo del sistema) y clona el proyecto:
```bash
git clone https://github.com/Nowaa-ff/Proyecto-Final.git
cd Proyecto-Final
```

### Paso 2: Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Paso 3: Instalar las dependencias
Ejecuta el siguiente comando para instalar `rich` y `openpyxl`:
```bash
pip install -r requirements.txt
```

### Paso 4: Iniciar la aplicación
Ejecuta el archivo principal:
```bash
python main.py
```

---

## Uso de Inteligencia Artificial

#### Durante el desarrollo se utilizaron herramientas de IA como asistentes de desarrollo: para generar ideas, depurar errores de sintaxis y estructurar la documentación.

#### Además, se utilizó Antigravity (entorno de desarrollo con agente de IA) para mejorar la portabilidad de la ejecución: los lanzadores iniciar.bat e iniciar.sh, la configuración opcional de Docker y Codespaces, y la actualización de esta documentación. La lógica del juego, las preguntas, el sistema de puntos y el diseño de la aplicación no fueron modificados por el agente. Todo el código fue revisado y es explicado por el autor.

---

## Créditos
- **Proyecto Final de Programación**
- Desarrollado en Python 3 para entorno escolar y educativo.
