Carpeta para funciones de apoyo (utilidades) que se usan en distintas partes del proyecto.

Ejemplos de módulos que podrías crear aquí:
  - paths.py        → manejo centralizado de rutas (assets, pdfs, ayuda, etc.)
  - loader.py       → funciones para cargar texto de ayuda o problemas desde archivos
  - validaciones.py → validaciones numéricas y de entrada de usuario
  - colores.py      → paleta de colores reutilizable para la interfaz
  - constantes.py   → diccionarios con configuraciones globales del juego

De esta forma, la lógica general no se mezcla con la interfaz ni con los métodos matemáticos.
