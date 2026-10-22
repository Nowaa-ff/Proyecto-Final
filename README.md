# Trivia App & Ranking Manager
Aplicación de consola interactiva para jugar a trivias de preguntas y respuestas, gestionar rankings de jugadores y exportar reportes estadísticos.

## Herramienta a desarrollar
Un sistema completo en consola que administra preguntas por categorías, controla el tiempo de respuesta de cada usuario, lleva un registro histórico de puntajes y exporta datos para análisis.

### Funcionalidades principales:
- **Menú interactivo:** Navegación sencilla entre jugar, ver estadísticas y exportar reportes.
- **Modo de juego dinámico:** Selección aleatoria de preguntas y temporizador para responder.
- **Panel visual en consola:** Tablas, barras de progreso y colores de estado para una interfaz intuitiva.
- **Módulo estadístico:** Cálculo automático del promedio de puntos por jugador y porcentaje de efectividad.
- **Exportación de reportes:** Generación automática de archivos Excel (`.xlsx`) con el historial de partidas.

## ¿Para qué sirve?
Sirve como herramienta de entretenimiento e interacción en consola, permitiendo a grupos de usuarios competir por puntajes, medir sus conocimientos en tiempo real y guardar un registro ordenado y exportable de su rendimiento.


## Bibliotecas utilizadas

### Módulos internos (Biblioteca estándar):
- `json`: Para cargar el banco de preguntas y almacenar la base de datos de usuarios.
- `random`: Para desordenar y seleccionar preguntas al azar en cada partida.
- `time`: Para medir el tiempo transcurrido en cada respuesta y aplicar penalizaciones.
- `datetime`: Para registrar la fecha y hora exacta de cada partida jugada.
- `statistics`: Para calcular promedios y métricas de desempeño de los jugadores.

### Bibliotecas externas:
- `rich`: Para renderizar la interfaz de usuario con paneles, tablas y colores en la terminal.
- `openpyxl`: Para estructurar y exportar la tabla de posiciones e historial a un archivo Excel (`.xlsx`).


## Plan de Trabajo y uso de IA
Para este proyecto **no se utilizará un agente autónomo de IA**. Se utilizaron herramientas de IA exclusivamente como asistentes de desarrollo para la generación de ideas, depuración de errores de sintaxis y estructuración de la documentación del proyecto.
