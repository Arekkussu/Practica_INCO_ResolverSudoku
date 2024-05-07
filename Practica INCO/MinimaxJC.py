import tkinter as tk
import copy
import time

# Variables globales para manejar el estado del juego y las puntuaciones
puntuacion_a = 0
puntuacion_b = 0
jugador_actual = 'A'  # Alternará entre 'A' y 'B'

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
    print(f"Jugador {jugador} ha realizado un movimiento en la posición ({i}, {j}) con el valor {valor}.")
    return nuevo_sudoku

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

def estrategia(sudoku, profundidad, es_maximizador, jugador, alpha, beta):
    print(f"Estrategia está evaluando un nodo con profundidad {profundidad}...")
    if profundidad == 0 or juego_terminado(sudoku):
        return evaluar_estado(sudoku, jugador)
    if es_maximizador:
        max_eval = float('-inf')
        for movimiento in posibles_movimientos(sudoku, jugador):
            copia_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
            evaluacion = estrategia(copia_sudoku, profundidad - 1, False, jugador, alpha, beta)
            max_eval = max(max_eval, evaluacion)
            alpha = max(alpha, evaluacion)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for movimiento in posibles_movimientos(sudoku, jugador):
            copia_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
            evaluacion = estrategia(copia_sudoku, profundidad - 1, True, jugador, alpha, beta)
            min_eval = min(min_eval, evaluacion)
            beta = min(beta, evaluacion)
            if beta <= alpha:
                break
        return min_eval


class SudokuGUI:
    def __init__(self, root, sudoku, jugador_actual='A'):
        self.root = root
        self.sudoku = sudoku
        self.jugador_actual = jugador_actual
        self.puntuacion_a = 0
        self.puntuacion_b = 0
        self.init_GUI()

    def init_GUI(self):
        self.root.title("Sudoku Competitivo")
        self.canvas = tk.Canvas(self.root, width=400, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Puntuación A y B en colores diferentes
        self.score_text_a = self.canvas.create_text(100, 425, text=f"Puntuación A: {self.puntuacion_a}",
                                                    font=('Helvetica', 12), fill="blue")
        self.score_text_b = self.canvas.create_text(300, 425, text=f"Puntuación B: {self.puntuacion_b}",
                                                    font=('Helvetica', 12), fill="black")

        # Dibujar celdas y números
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        cell_width = 400 // 9
        cell_height = 400 // 9
        for i in range(9):
            for j in range(9):
                x1, y1 = j * cell_width, i * cell_height
                x2, y2 = x1 + cell_width, y1 + cell_height
                color = "red" if self.sudoku[i][j] != 0 else "white"
                self.cells[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if self.sudoku[i][j] != 0:
                    self.canvas.create_text(x1 + cell_width // 2, y1 + cell_height // 2, text=str(self.sudoku[i][j]), fill="black")

        # Botón para resolver Sudoku
        self.Consejo_text = self.canvas.create_text(200, 475, text=f"Pulse el siguiente botón para comenzar la ejecución.\n     Después, espere a que el algoritmo se ejecute",
                                                    font=('Helvetica', 12), fill="black")
        self.solve_button = tk.Button(self.root, text="Resolver Sudoku", command=self.resolver_sudoku)
        self.solve_button.pack()


    def update_board(self, movimiento, valor, jugador):
        i, j = movimiento
        color = "blue" if jugador == 'A' else "black"
        cell_width = 400 // 9
        cell_height = 400 // 9
        x1, y1 = j * cell_width, i * cell_height
        self.canvas.itemconfig(self.cells[i][j], fill=color)
        self.canvas.create_text(x1 + cell_width // 2, y1 + cell_height // 2, text=str(valor), fill="white")
        # Actualizar puntuaciones
        if jugador == 'A':
            self.puntuacion_a += 1
            self.canvas.itemconfig(self.score_text_a, text=f"Puntuación A: {self.puntuacion_a}")
        else:
            self.puntuacion_b += 1
            self.canvas.itemconfig(self.score_text_b, text=f"Puntuación B: {self.puntuacion_b}")

        print(f"Se ha actualizado la interfaz con el movimiento del Jugador {jugador}.")

    def resolver_sudoku(self):
        global jugador_actual, puntuacion_a, puntuacion_b
        while not juego_terminado(self.sudoku):
            if self.jugador_actual == 'A':
                jugador = 'A'
                self.jugador_actual = 'B'
            else:
                jugador = 'B'
                self.jugador_actual = 'A'
            movimiento = self.mejor_movimiento(self.sudoku, jugador)
            self.sudoku = realizar_movimiento(self.sudoku, movimiento, jugador)
            self.update_board((movimiento[0], movimiento[1]), movimiento[2], jugador)
            time.sleep(1)  # Espera para visualizar los movimientos

    def mejor_movimiento(self, sudoku, jugador):
        movimientos = posibles_movimientos(sudoku, jugador)
        mejor_movimiento = None
        mejor_evaluacion = float('-inf') if jugador == 'A' else float('inf')
        for movimiento in movimientos:
            copia_sudoku = realizar_movimiento(sudoku, movimiento, jugador)
            evaluacion = estrategia(copia_sudoku, 2, False, jugador, float('-inf'), float('inf'))
            if (jugador == 'A' and evaluacion > mejor_evaluacion) or (jugador == 'B' and evaluacion < mejor_evaluacion):
                mejor_evaluacion = evaluacion
                mejor_movimiento = movimiento
        return mejor_movimiento

def mostrar_sudoku(sudoku):
    root = tk.Tk()
    app = SudokuGUI(root, sudoku)
    root.mainloop()

import unittest

class TestSudokuLogic(unittest.TestCase):
    def test_es_movimiento_valido(self):
        sudoku = [[0]*9 for _ in range(9)]
        sudoku[0][0] = 5
        self.assertFalse(es_movimiento_valido(sudoku, 0, 1, 5))  # Mismo número en la fila
        self.assertTrue(es_movimiento_valido(sudoku, 0, 1, 6))  # Número válido

    def test_realizar_movimiento(self):
        sudoku = [[0]*9 for _ in range(9)]
        movimiento = (0, 0, 5)
        resultado = realizar_movimiento(sudoku, movimiento, 'A')
        self.assertEqual(resultado[0][0], 5)

    def test_juego_terminado(self):
        sudoku = [[1]*9 for _ in range(9)]
        self.assertTrue(juego_terminado(sudoku))

# Correr las pruebas
if __name__ == '__main__':
    unittest.main()
