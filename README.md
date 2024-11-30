# Ajedrez por Consola con Minimax y Poda Alfa-Beta

Este proyecto implementa un juego de ajedrez por consola diseñado para probar el algoritmo **Minimax** con **poda alfa-beta**. Ha sido desarrollado como parte de la especialización en Inteligencia Artificial, con el objetivo de demostrar la capacidad de la IA para tomar decisiones estratégicas y maximizar su puntaje.

## **Características del Proyecto**

- **Jugador humano**: Controla las piezas blancas (`Blancas`).
- **Inteligencia artificial (IA)**: Controla las piezas negras (`Negras`), implementando el algoritmo Minimax con poda alfa-beta para optimizar sus decisiones.
- **Interfaz por consola**: 
  - El jugador selecciona la pieza a mover (por coordenadas, como `E2`).
  - El sistema muestra todas las jugadas posibles para esa pieza.
  - El jugador elige un destino para mover la pieza.
- **Turnos alternados**:
  - Primero juega el humano (fichas blancas).
  - Luego, la IA toma su turno con las piezas negras.
  - La IA analiza posibles movimientos para maximizar su puntaje.

## **Ejecución del Proyecto**

### **Requisitos previos**
- **Python 3.8+** instalado en el sistema (para ejecutar el script original).
- O un sistema operativo compatible para ejecutar el archivo ejecutable generado.

### **Opciones de ejecución**

#### 1. **Ejecutar el script `ajedrez.py`**
1. Abre una terminal y navega hasta el directorio donde se encuentra el archivo `ajedrez.py`.
2. Ejecuta el script con:
   ```bash
   python ajedrez.py

#### 2. **Ejecutar el archivo ejecutable**
Si prefieres no instalar Python, puedes usar el archivo ejecutable que se encuentra en la carpeta `dist`. Este archivo ha sido generado con PyInstaller y no requiere dependencias adicionales:
1. Navega a la carpeta `dist` dentro del proyecto.
2. Ejecuta el archivo:
   - **En Windows**:
     ```bash
     dist\ajedrez.exe
     ```
   - **En Linux/macOS**:
     ```bash
     ./dist/ajedrez
     ./ajedrez
     ```
### **Cómo jugar**
1. Sigue las instrucciones en pantalla:
   - Selecciona una pieza blanca que deseas mover introduciendo su coordenada inicial (por ejemplo, `E2`).
   - Revisa las posibles jugadas mostradas por el sistema.
   - Introduce la coordenada de destino para completar tu jugada.
2. La IA tomará su turno automáticamente con las piezas negras, buscando maximizar su puntaje mediante el algoritmo Minimax.

### **Reglas y Notas**
- El juego sigue las reglas estándar del ajedrez.
- Los movimientos válidos se verifican según el tipo de pieza y las condiciones del tablero.
- El algoritmo Minimax evalúa los movimientos posibles y utiliza poda alfa-beta para reducir el espacio de búsqueda y tomar decisiones más eficientes.

### **Objetivos de la IA**
- Maximizar su puntaje capturando piezas blancas de mayor valor.
- Controlar posiciones estratégicas, como el centro del tablero.
- Realizar movimientos válidos según las reglas del ajedrez.

### **Contribución**
Este proyecto está enfocado en mostrar la integración de un algoritmo de inteligencia artificial en un entorno práctico. Si encuentras errores o deseas sugerir mejoras, siéntete libre de contribuir.

MARIA ISABEL MARIN HENAO
LUIS ALEXANDER CASTAÑO REYES
GUSTAVO ANDRES GOMEZ BONILLA