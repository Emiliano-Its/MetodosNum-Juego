PROYECTO: Juego de Métodos Numéricos - Math Defuser (versión reorganizada mínima)
-------------------------------------------------------------------------------

Esta versión fue limpiada y reorganizada para que sea más fácil de mantener.

Estructura actual:
  - main.py        → Punto de entrada del programa (lanza la interfaz gráfica).
  - interfaz.py    → Contiene la clase principal MathDefuserGame y toda la lógica de UI.
  - metodos.py     → Contiene la clase MetodosCalculo con todos los métodos numéricos
                     y generadores de problemas.
  - assets/        → Imágenes, iconos y recursos gráficos.
  - pdfs/          → Archivos PDF de teoría y ejercicios por tema.
  - ayuda/         → (NUEVO) Archivos de texto para mostrar ayuda rápida dentro del juego.
  - utils/         → (NUEVO) Carpeta reservada para funciones de apoyo reutilizables.

Carpetas que se eliminaron en esta reorganización:
  - .idea/         → Archivos específicos del IDE (PyCharm), no necesarios para ejecutar.
  - __pycache__/   → Archivos compilados .pyc, se regeneran automáticamente.
  - "Metodos PIA"/ → Copia duplicada del proyecto dentro del propio proyecto.

Cómo ejecutar:
  1. Asegúrate de tener Python instalado.
  2. Abre una terminal en esta carpeta (donde está main.py).
  3. Ejecuta:  python main.py

NOTA:
  La lógica del juego sigue funcionando igual que en la versión original.
  Sólo se limpió y organizó la estructura de archivos para facilitar futuras
  modificaciones, como:
    - Agregar nuevos métodos numéricos.
    - Vincular textos de ayuda (carpeta ayuda/).
    - Añadir nuevas pantallas (victoria/derrota) desde interfaz.py.
