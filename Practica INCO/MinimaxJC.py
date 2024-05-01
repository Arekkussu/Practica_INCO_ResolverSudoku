import tkinter as tk
import copy

def es_movimiento_valido(sudoku, i, j, valor):
    """ Verifica si es válido colocar el valor en la celda (i, j). """
    # Verificar fila y columna
    for k in range(9):
        if sudoku[i][k] == valor or sudoku[k][j] == valor:
            return False
    # Verificar el subgrupo 3x3
    start_i, start_j = 3 * (i // 3), 3 * (j // 3)
    for x in range(3):
        for y in range(3):
            if sudoku[start_i + x][start_j + y] == valor:
                return False
    return True

def realizar_movimiento(sudoku, movimiento, jugador):
    """ Realiza un movimiento en el tablero y actualiza el estado. """
    i, j, valor = movimiento
    nuevo_sudoku = copy.deepcopy(sudoku)
    nuevo_sudoku[i][j] = valor
    return nuevo_sudoku

def evaluar_estado(sudoku, jugador):
    """ Evalúa el estado actual del juego para un jugador específico. """
    if juego_terminado(sudoku):
        return float('inf') if jugador == "jugador_actual" else float('-inf')
    puntos = sum(calcular_puntuacion(sudoku, (i, j, sudoku[i][j]), jugador)
                 for i in range(9) for j in range(9) if sudoku[i][j] != 0)
    return puntos

def posibles_movimientos(sudoku, jugador):
    """ Devuelve una lista de todos los movimientos válidos para un jugador. """
    movimientos = []
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:  # Casilla vacía
                for valor in range(1, 10):
                    if es_movimiento_valido(sudoku, i, j, valor):
                        movimientos.append((i, j, valor))
    return movimientos
def calcular_puntuacion(sudoku, movimiento, jugador):
    i, j, valor = movimiento
    puntos = 0

    # Comprobar si el movimiento es válido
    if es_movimiento_valido(sudoku, i, j, valor):
        puntos += 1  # Punto por colocar un número
        # Hacer el movimiento para evaluación
        nuevo_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
        # Comprobar filas, columnas y subgrupos completos
        if fila_completa(nuevo_sudoku, i):
            puntos += 3
        if columna_completa(nuevo_sudoku, j):
            puntos += 3
        if subgrupo_completo(nuevo_sudoku, i, j):
            puntos += 3
    else:
        puntos -= 2  # Penalización por error

    return puntos

def fila_completa(sudoku, fila):
    return all(sudoku[fila][j] != 0 for j in range(9))

def columna_completa(sudoku, columna):
    return all(sudoku[i][columna] != 0 for i in range(9))

def subgrupo_completo(sudoku, i, j):
    start_i, start_j = 3 * (i // 3), 3 * (j // 3)
    return all(sudoku[start_i + x][start_j + y] != 0 for x in range(3) for y in range(3))
def juego_terminado(sudoku):
    """ Determina si el juego ha terminado, ya sea completando el Sudoku o por errores irreparables. """
    if hay_errores_irreparables(sudoku):
        print("Error irreparable detectado. Juego terminado.")
        return True

    lleno = all(all(celda != 0 for celda in fila) for fila in sudoku)
    if lleno and all(fila_completa(sudoku, i) and columna_completa(sudoku, j) for i in range(9) for j in range(9)):
        print("Sudoku completado correctamente. Juego terminado.")
        return True

    return False

def hay_errores_irreparables(sudoku):
    """ Verifica si hay errores que hacen que el juego no pueda continuar. """
    # Comprobar duplicados en filas y columnas
    for i in range(9):
        if tiene_duplicados(sudoku[i]):  # Revisar fila i
            return True
        columna = [sudoku[x][i] for x in range(9)]
        if tiene_duplicados(columna):  # Revisar columna i
            return True

    # Comprobar duplicados en cada subcuadro 3x3
    for start_i in range(0, 9, 3):
        for start_j in range(0, 9, 3):
            subcuadro = [sudoku[start_i + x][start_j + y] for x in range(3) for y in range(3)]
            if tiene_duplicados(subcuadro):
                return True

    return False

def tiene_duplicados(lista):
    """ Verifica si una lista contiene duplicados, ignorando los ceros. """
    elementos = set()
    for item in lista:
        if item != 0:
            if item in elementos:
                return True
            elementos.add(item)
    return False

def minimax_decision(sudoku, profundidad, jugador):
    """ Decidir el mejor movimiento utilizando la función Minimax. """
    best_score = float('-inf') if jugador == 'A' else float('inf')
    best_move = None
    for movimiento in posibles_movimientos(sudoku, jugador):
        copia_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
        score = minimax(copia_sudoku, profundidad - 1, jugador == 'B', jugador, alpha=float('-inf'), beta=float('inf'))
        if jugador == 'A' and score > best_score:
            best_score, best_move = score, movimiento
        elif jugador == 'B' and score < best_score:
            best_score, best_move = score, movimiento
    return best_move

def minimax(sudoku, profundidad, es_maximizador, jugador, alpha, beta):
    if profundidad == 0 or juego_terminado(sudoku):
        return evaluar_estado(sudoku, jugador)

    if es_maximizador:
        max_eval = float('-inf')
        for movimiento in posibles_movimientos(sudoku, jugador):
            copia_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
            evaluacion = minimax(copia_sudoku, profundidad - 1, False, jugador, alpha, beta)
            max_eval = max(max_eval, evaluacion)
            alpha = max(alpha, evaluacion)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for movimiento in posibles_movimientos(sudoku, jugador):
            copia_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
            evaluacion = minimax(copia_sudoku, profundidad - 1, True, jugador, alpha, beta)
            min_eval = min(min_eval, evaluacion)
            beta = min(beta, evaluacion)
            if beta <= alpha:
                break
        return min_eval
def mostrar_sudoku(sudoku, mensaje):
    global label_mensaje, label_puntuacion_a, label_puntuacion_b

    label_mensaje.config(text=mensaje)
    label_puntuacion_a.config(text=f"Puntuación Jugador A: {puntuacion_a}")
    label_puntuacion_b.config(text=f"Puntuación Jugador B: {puntuacion_b}")

    # Limpiar el marco actual del Sudoku
    for widget in marco_sudoku.winfo_children():
        widget.destroy()

    # Rellenar el marco con los números actuales del Sudoku
    for i in range(9):
        for j in range(9):
            numero = sudoku[i][j] if sudoku[i][j] != 0 else ""
            celda = tk.Label(marco_sudoku, text=str(numero), width=2, height=1, font=("Helvetica", 16),
                             borderwidth=1, relief="solid")
            celda.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)


def actualizar_juego(sudoku, jugador, i, j, valor):
    """ Realiza y muestra un movimiento, actualiza puntuaciones y maneja la alternancia de turnos. """
    global puntuacion_a, puntuacion_b, jugador_actual
    nuevo_sudoku = realizar_movimiento(sudoku, (i, j, valor), jugador)
    puntuacion = calcular_puntuacion(sudoku, (i, j, valor), jugador)

    if jugador == 'A':
        puntuacion_a += puntuacion
    else:
        puntuacion_b += puntuacion

    # Comprobación de finalización del juego
    if juego_terminado(nuevo_sudoku):
        ganador = 'Jugador A' if puntuacion_a > puntuacion_b else 'Jugador B'
        mensaje = f"SUDOKU COMPLETADO, GANADOR: {ganador}"
        mostrar_sudoku(nuevo_sudoku, mensaje)
    else:
        jugador_actual = 'A' if jugador_actual == 'B' else 'B'
        mensaje = f"TURNO JUGADOR {jugador_actual}, PUNTUACIÓN ACCIÓN: {puntuacion}"
        mostrar_sudoku(nuevo_sudoku, mensaje)

def jugar_sudoku(sudoku):
    global puntuacion_a, puntuacion_b, jugador_actual
    mensaje = "El juego está en curso."

    while not juego_terminado(sudoku):
        movimiento = minimax_decision(sudoku, 3, jugador_actual)
        if movimiento:
            sudoku = realizar_movimiento(sudoku, movimiento, jugador_actual)
            puntuacion = calcular_puntuacion(sudoku, movimiento, jugador_actual)
            if jugador_actual == 'A':
                puntuacion_a += puntuacion
            else:
                puntuacion_b += puntuacion
            jugador_actual = 'B' if jugador_actual == 'A' else 'A'
        else:
            mensaje = "No hay movimientos válidos disponibles. Juego finalizado."
            break

    if juego_terminado(sudoku):
        ganador = 'Jugador A' if puntuacion_a > puntuacion_b else 'Jugador B'
        if hay_errores_irreparables(sudoku):
            mensaje = "Error irreparable detectado. Juego finalizado."
        else:
            mensaje = f"Sudoku completado correctamente. Ganador: {ganador}"

    mostrar_resultado_final(sudoku, puntuacion_a, puntuacion_b, mensaje)


# Variables globales para manejar el estado del juego y las puntuaciones
puntuacion_a = 0
puntuacion_b = 0
jugador_actual = 'A'  # Alternará entre 'A' y 'B'
ventana = None
marco_sudoku = None
label_mensaje = None
label_puntuacion_a = None
label_puntuacion_b = None

def crear_ventana():
    global ventana, marco_sudoku, label_mensaje, label_puntuacion_a, label_puntuacion_b
    ventana = tk.Tk()
    ventana.title("Sudoku Competitivo")
    ventana.geometry("450x550")

    label_mensaje = tk.Label(ventana, text="INICIO DEL JUEGO", font=("Helvetica", 14))
    label_mensaje.pack(pady=(5, 10))

    marco_sudoku = tk.Frame(ventana)
    marco_sudoku.pack(pady=(0, 20))

    label_puntuacion_a = tk.Label(ventana, text=f"Puntuación Jugador A: {puntuacion_a}", font=("Helvetica", 12))
    label_puntuacion_a.pack()

    label_puntuacion_b = tk.Label(ventana, text=f"Puntuación Jugador B: {puntuacion_b}", font=("Helvetica", 12))
    label_puntuacion_b.pack()

    return ventana

def mostrar_resultado_final(sudoku, puntuacion_a, puntuacion_b, mensaje):
    """ Muestra el estado final del Sudoku y las puntuaciones de los jugadores. """
    ventana_final = tk.Tk()
    ventana_final.title("Resultado Final del Sudoku Competitivo")
    ventana_final.geometry("450x600")

    tk.Label(ventana_final, text="Sudoku Final", font=("Helvetica", 20, "bold")).pack(pady=(10, 5))
    tk.Label(ventana_final, text=mensaje, font=("Helvetica", 14, "bold")).pack(pady=(5, 10))

    marco_sudoku = tk.Frame(ventana_final)
    marco_sudoku.pack(pady=(0, 20))

    for i in range(9):
        for j in range(9):
            numero = sudoku[i][j] if sudoku[i][j] != 0 else ""
            celda = tk.Label(marco_sudoku, text=str(numero), width=2, height=1, font=("Helvetica", 16),
                             borderwidth=1, relief="solid")
            celda.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

    tk.Label(ventana_final, text=f"Puntuación Jugador A: {puntuacion_a}", font=("Helvetica", 14)).pack()
    tk.Label(ventana_final, text=f"Puntuación Jugador B: {puntuacion_b}", font=("Helvetica", 14)).pack()

    ventana_final.mainloop()
