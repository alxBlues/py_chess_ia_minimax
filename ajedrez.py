import math

# Representación inicial del tablero de ajedrez
tablero = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],  # Piezas negras
    ["p", "p", "p", "p", "p", "p", "p", "p"],  # Peones negros
    [".", ".", ".", ".", ".", ".", ".", "."],  # Casillas vacías
    [".", ".", ".", ".", ".", ".", ".", "."],  # Casillas vacías
    [".", ".", ".", ".", ".", ".", ".", "."],  # Casillas vacías
    [".", ".", ".", ".", ".", ".", ".", "."],  # Casillas vacías
    ["P", "P", "P", "P", "P", "P", "P", "P"],  # Peones blancos
    ["R", "N", "B", "Q", "K", "B", "N", "R"],  # Piezas blancas
]

historial_movimientos = []  # Lista global para almacenar los movimientos recientes

tableros_visitados = set()  # Para almacenar estados de tableros ya evaluados

# Valores de las piezas
valores_piezas = {
    "p": 10,  # Peón
    "n": 30,  # Caballo
    "b": 30,  # Alfil
    "r": 50,  # Torre
    "q": 90,  # Reina
    "k": 900,  # Rey
}

# Puntuaciones de los jugadores
puntaje = {"blancas": 0, "negras": 0}


# Función para imprimir el tablero
def imprimir_tablero():
    print("  A B C D E F G H")  # Coordenadas horizontales
    for i, fila in enumerate(tablero, start=1):
        print(f"{i} {' '.join(fila)}")  # Coordenadas verticales
    print()


# Función para traducir coordenadas como E2 a índices del tablero
def traducir_coordenadas(coordenada):
    columna = ord(coordenada[0].upper()) - ord("A")  # A=0, B=1, ..., H=7
    fila = int(coordenada[1]) - 1  # La fila coincide directamente con los índices de la matriz
    return fila, columna

def validar_coordenada(coordenada):
    """
    Verifica si una coordenada está dentro del rango válido (A1-H8).
    """
    if len(coordenada) != 2:
        return False
    columna, fila = coordenada[0], coordenada[1]
    if columna not in "ABCDEFGH":
        return False
    if not fila.isdigit() or not (1 <= int(fila) <= 8):
        return False
    return True

def validar_movimiento(origen, destino, jugador):
    """
    Verifica si un movimiento es válido según las reglas del ajedrez.
    """
    fila_ori, col_ori = traducir_coordenadas(origen)
    fila_des, col_des = traducir_coordenadas(destino)
    pieza = tablero[fila_ori][col_ori]
    
    print(f"Validando movimiento {origen} -> {destino} para {jugador}, pieza: {pieza}")

    # Verificar que hay una pieza en la casilla de origen
    if pieza == ".":
        return False, "No hay ninguna pieza en la casilla de origen."

    # Verificar que la pieza corresponde al turno actual
    if jugador == "blancas" and pieza.islower():
        return False, "No puedes mover piezas negras."
    if jugador == "negras" and pieza.isupper():
        return False, "No puedes mover piezas blancas."

    # Validar el movimiento según las reglas de la pieza
    if not es_movimiento_valido(pieza, fila_ori, col_ori, fila_des, col_des):
        return False, "El movimiento no es válido para esta pieza."

    return True, "Movimiento válido."


def no_hay_obstaculos(fila_ori, col_ori, fila_des, col_des):
    """Verifica si el camino está libre entre la casilla de origen y destino."""
    if fila_ori == fila_des:  # Movimiento horizontal
        paso = 1 if col_des > col_ori else -1
        for c in range(col_ori + paso, col_des, paso):
            if tablero[fila_ori][c] != ".":
                return False
    elif col_ori == col_des:  # Movimiento vertical
        paso = 1 if fila_des > fila_ori else -1
        for f in range(fila_ori + paso, fila_des, paso):
            if tablero[f][col_ori] != ".":
                return False
    else:  # Movimiento diagonal
        paso_f = 1 if fila_des > fila_ori else -1
        paso_c = 1 if col_des > col_ori else -1
        for f, c in zip(range(fila_ori + paso_f, fila_des, paso_f), range(col_ori + paso_c, col_des, paso_c)):
            if tablero[f][c] != ".":
                return False
    return True


def es_movimiento_valido(pieza, fila_ori, col_ori, fila_des, col_des):
    """
    Verifica si el movimiento de la pieza es válido según sus reglas específicas.
    """
    # No permitir que una pieza se mueva a su misma posición
    if fila_ori == fila_des and col_ori == col_des:
        return False

    destino_pieza = tablero[fila_des][col_des]

    # Verificar que no captura una pieza propia
    if (pieza.isupper() and destino_pieza.isupper()) or (pieza.islower() and destino_pieza.islower()):
        return False

    # Peón
    if pieza.lower() == "p":
        if pieza.isupper():  # Peón blanco
            if fila_ori - fila_des == 1 and col_ori == col_des and destino_pieza == ".":
                return True
            if fila_ori == 6 and fila_ori - fila_des == 2 and col_ori == col_des and \
                    destino_pieza == "." and tablero[fila_ori - 1][col_des] == ".":
                return True
            if fila_ori - fila_des == 1 and abs(col_ori - col_des) == 1 and destino_pieza.islower():
                return True
        else:  # Peón negro
            if fila_des - fila_ori == 1 and col_ori == col_des and destino_pieza == ".":
                return True
            if fila_ori == 1 and fila_des - fila_ori == 2 and col_ori == col_des and \
                    destino_pieza == "." and tablero[fila_ori + 1][col_des] == ".":
                return True
            if fila_des - fila_ori == 1 and abs(col_ori - col_des) == 1 and destino_pieza.isupper():
                return True

    # Torre
    elif pieza.lower() == "r":
        if fila_ori == fila_des or col_ori == col_des:
            return no_hay_obstaculos(fila_ori, col_ori, fila_des, col_des) and destino_pieza != pieza

    # Caballo
    elif pieza.lower() == "n":
        if (abs(fila_ori - fila_des) == 2 and abs(col_ori - col_des) == 1) or \
           (abs(fila_ori - fila_des) == 1 and abs(col_ori - col_des) == 2):
            return True

    # Alfil
    elif pieza.lower() == "b":
        if abs(fila_ori - fila_des) == abs(col_ori - col_des):
            return no_hay_obstaculos(fila_ori, col_ori, fila_des, col_des)

    # Reina
    elif pieza.lower() == "q":
        if fila_ori == fila_des or col_ori == col_des or abs(fila_ori - fila_des) == abs(col_ori - col_des):
            return no_hay_obstaculos(fila_ori, col_ori, fila_des, col_des)

    # Rey
    elif pieza.lower() == "k":
        if abs(fila_ori - fila_des) <= 1 and abs(col_ori - col_des) <= 1:
            return True

    return False


def mover_pieza(origen, destino, jugador):
    """
    Realiza el movimiento de la ficha en el tablero.
    Si se captura una ficha, se actualiza el puntaje.
    """
    global puntaje, historial_movimientos
    fila_ori, col_ori = traducir_coordenadas(origen)
    fila_des, col_des = traducir_coordenadas(destino)

    pieza = tablero[fila_ori][col_ori]
    ficha_capturada = tablero[fila_des][col_des]

    if ficha_capturada != ".":
        ficha_capturada_valor = valores_piezas[ficha_capturada.lower()]
        puntaje[jugador] += ficha_capturada_valor
        print(f"{jugador.capitalize()} capturó una ficha enemiga ({ficha_capturada}) y ganó {ficha_capturada_valor} puntos!")

    tablero[fila_ori][col_ori] = "."
    tablero[fila_des][col_des] = pieza

    # Actualizar historial de movimientos
    historial_movimientos.append((origen, destino))
    if len(historial_movimientos) > 10:
        historial_movimientos.pop(0)


def reiniciar_tablero():
    global tablero, puntaje
    tablero = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]
    puntaje = {"blancas": 0, "negras": 0}
    print("¡El tablero se ha reiniciado!")


def obtener_movimientos_posibles(origen, jugador):
    """
    Devuelve una lista de movimientos válidos para una pieza en la posición 'origen'.
    """
    fila_ori, col_ori = traducir_coordenadas(origen)
    pieza = tablero[fila_ori][col_ori]
    movimientos = []

    # Asegúrate de que se validen correctamente las piezas
    if (jugador == "blancas" and pieza.isupper()) or (jugador == "negras" and pieza.islower()):
        for fila_des in range(8):
            for col_des in range(8):
                destino = f"{chr(col_des + 65)}{8 - fila_des}"
                valido, _ = validar_movimiento(origen, destino, jugador)
                if valido:
                    movimientos.append(destino)

    return movimientos

def evaluacion(origen, jugador):
    """
    Evalúa las jugadas posibles para una ficha y devuelve un diccionario con los destinos
    y sus valores basados en capturas.
    """
    fila_ori, col_ori = traducir_coordenadas(origen)
    pieza = tablero[fila_ori][col_ori]
    movimientos = obtener_movimientos_posibles(origen, jugador)

    resultados = {}
    for destino in movimientos:
        fila_des, col_des = traducir_coordenadas(destino)
        destino_pieza = tablero[fila_des][col_des]

        # Si el destino tiene una pieza contraria, agrega su valor
        if destino_pieza != ".":
            resultados[destino] = valores_piezas[destino_pieza.lower()]
        else:
            resultados[destino] = 0  # Movimiento sin captura

    return resultados

# SOLO IA  MINIMAX SIN PODA ALFA BETA 


def obtener_piezas(jugador, tablero):
    """
    Devuelve una lista de coordenadas de todas las piezas del jugador actual.
    """
    piezas = []
    for fila_idx, fila in enumerate(tablero):  # fila_idx: 0-7
        for col_idx, pieza in enumerate(fila):  # col_idx: 0-7
            # Identifica piezas del jugador
            if jugador == "blancas" and pieza.isupper():  # Piezas blancas en mayúscula
                # Corrige las filas para que '8' sea fila_idx 0 y '1' sea fila_idx 7
                piezas.append(f"{chr(col_idx + 65)}{fila_idx + 1}")
            elif jugador == "negras" and pieza.islower():  # Piezas negras en minúscula
                piezas.append(f"{chr(col_idx + 65)}{fila_idx + 1}")
    return piezas

# Función Minimax adaptada para tu entorno
def minimax(tablero, profundidad, alpha, beta, maximizando, jugador):
    """
    Algoritmo Minimax con poda alfa-beta mejorado para evitar ciclos y considerar penalizaciones.
    """
    if profundidad == 0 or str(tablero) in tableros_visitados:
        return evaluar_tablero(tablero), None

    tableros_visitados.add(str(tablero))  # Evitar repetir tableros
    mejor_movimiento = None
    siguiente_jugador = "blancas" if jugador == "negras" else "negras"

    if maximizando:
        max_eval = -math.inf
        piezas_jugador = obtener_piezas(jugador, tablero)
        for origen in piezas_jugador:
            movimientos = obtener_movimientos_posibles(origen, jugador)
            for destino in movimientos:
                nuevo_tablero = simular_movimiento(tablero, origen, destino)
                evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, alpha, beta, False, siguiente_jugador)
                
                # Penalización por movimientos repetitivos
                if (origen, destino) in historial_movimientos:
                    evaluacion -= 10

                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_movimiento = (origen, destino)
                alpha = max(alpha, evaluacion)

                if beta <= alpha:
                    break

        return max_eval, mejor_movimiento
    else:
        min_eval = math.inf
        piezas_jugador = obtener_piezas(jugador, tablero)
        for origen in piezas_jugador:
            movimientos = obtener_movimientos_posibles(origen, jugador)
            for destino in movimientos:
                nuevo_tablero = simular_movimiento(tablero, origen, destino)
                evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, alpha, beta, True, siguiente_jugador)
                
                if (origen, destino) in historial_movimientos:
                    evaluacion += 10

                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_movimiento = (origen, destino)
                beta = min(beta, evaluacion)

                if beta <= alpha:
                    break

        return min_eval, mejor_movimiento

# Función para que la IA juegue su turno
def turno_ia(tablero, jugador):
    """
    Ejecuta el turno de la IA (negras) utilizando el algoritmo Minimax.
    """
    global tableros_visitados
    tableros_visitados.clear()  # Reinicia el conjunto para este turno

    print("La IA está calculando su movimiento...")
    piezas_jugador = obtener_piezas(jugador, tablero)
    print(f"Piezas de {jugador}: {piezas_jugador}")
    for pieza in piezas_jugador:
        movimientos = obtener_movimientos_posibles(pieza, jugador)
        print(f"Pieza: {pieza}, Movimientos: {movimientos}")
    
    _, mejor_movimiento = minimax(tablero, profundidad=2, alpha=-math.inf, beta=math.inf, maximizando=True, jugador=jugador)

    if mejor_movimiento:
        origen, destino = mejor_movimiento
        print(f"La IA mueve de {origen} a {destino}")
        mover_pieza(origen, destino, jugador)
    else:
        print("La IA no tiene movimientos válidos. Ganan las blancas.")
# Evaluación básica del tablero
def evaluar_tablero(tablero):
    """
    Evalúa el tablero basado en la diferencia de valores de piezas, movilidad y control del centro.
    """
    puntaje_blancas = 0
    puntaje_negras = 0
    centro = [(3, 3), (3, 4), (4, 3), (4, 4)]  # Coordenadas del centro

    for fila_idx, fila in enumerate(tablero):
        for col_idx, pieza in enumerate(fila):
            if pieza != ".":
                valor = valores_piezas[pieza.lower()]
                if (fila_idx, col_idx) in centro:
                    valor += 5  # Bonus por control del centro
                if pieza.isupper():
                    puntaje_blancas += valor
                else:
                    puntaje_negras += valor

    return puntaje_negras - puntaje_blancas  # La IA maximiza negras

# Simulación de movimiento en un tablero
def simular_movimiento(tablero, origen, destino):
    """
    Crea una copia del tablero y realiza un movimiento.
    """
    fila_ori, col_ori = traducir_coordenadas(origen)
    fila_des, col_des = traducir_coordenadas(destino)
    nuevo_tablero = [fila.copy() for fila in tablero]  # Copia profunda
    nuevo_tablero[fila_des][col_des] = nuevo_tablero[fila_ori][col_ori]
    nuevo_tablero[fila_ori][col_ori] = "."
    return nuevo_tablero

# SOLO IA MINIMAX SIN PODA ALFA BETA
# Modificación en `jugar_ajedrez` para usar `evaluacion`
def jugar_ajedrez():
    """
    Controla el flujo del juego de ajedrez, alternando turnos entre blancas y negras.
    """
    jugador = "blancas"
    imprimir_tablero()

    while True:
        print(f"Turno de {jugador}.")
        print(f"Puntaje: Blancas {puntaje['blancas']} - Negras {puntaje['negras']}")

        if jugador == "negras":
            turno_ia(tablero, jugador)  # Ahora pasa el tablero correctamente
        else:
            while True:  # Bucle para asegurar que la entrada sea válida
                origen = input("Selecciona una ficha para mover (ejemplo: E2) o escribe 'reiniciar': ").strip().upper()

                if origen == "REINICIAR":
                    reiniciar_tablero()
                    imprimir_tablero()
                    continue

                if validar_coordenada(origen):
                    break
                else:
                    print("Entrada inválida. Asegúrate de usar un formato como 'E2'.")

            movimientos_posibles = obtener_movimientos_posibles(origen, jugador)
            if not movimientos_posibles:
                print("No hay movimientos válidos para esta ficha.")
                continue

            print(f"Movimientos posibles: {', '.join(movimientos_posibles)}")

            while True:  # Bucle para validar el destino
                destino = input("Selecciona el destino: ").strip().upper()

                if validar_coordenada(destino) and destino in movimientos_posibles:
                    break
                else:
                    print("Movimiento inválido. Selecciona un destino de la lista de movimientos posibles.")

            mover_pieza(origen, destino, jugador)

        imprimir_tablero()
        jugador = "negras" if jugador == "blancas" else "blancas"

jugar_ajedrez()