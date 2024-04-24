import tkinter as tk
import time

def avara(sudoku, mostrar=True):
# Definición de la función para encontrar la ubicación vacía con la heurística
    def find_empty_location_heuristic(board):
        min_options = float('inf')  # Inicializa la mínima cantidad de opciones con infinito
        empty_row, empty_col = None, None  # Inicializa las coordenadas de la celda vacía como nulas

        # Itera sobre todas las celdas del tablero
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:  # Verifica si la celda está vacía
                    options = count_options(board, i, j)  # Cuenta las opciones para esta celda
                    if options < min_options:  # Si esta celda tiene menos opciones que la mínima actual
                        min_options = options  # Actualiza la mínima cantidad de opciones
                        empty_row, empty_col = i, j  # Actualiza las coordenadas de la celda vacía

        return empty_row, empty_col  # Devuelve las coordenadas de la celda vacía con la mínima cantidad de opciones

    # Función para contar las opciones disponibles para una celda específica
    def count_options(board, row, col):
        options = 0  # Inicializa el contador de opciones

        # Itera sobre los números del 1 al 9
        for num in range(1, 10):
            # Verifica si el número puede ser colocado en la celda
            if is_valid_move(board, row, col, num):
                options += 1  # Incrementa el contador de opciones

        return options  # Devuelve la cantidad de opciones disponibles para la celda

    # Función principal para resolver el Sudoku utilizando la heurística
    def solve_sudoku_heuristic(board):
        row, col = find_empty_location_heuristic(board)  # Encuentra la celda vacía con la heurística
        if row is None:  # Si no hay celdas vacías
            return True  # El Sudoku está resuelto

        # Itera sobre los números del 1 al 9
        for num in range(1, 10):
            # Si el número es válido para colocar en la celda
            if is_valid_move(board, row, col, num):
                board[row][col] = num  # Coloca el número en la celda

                # Intenta resolver el Sudoku recursivamente
                if solve_sudoku_heuristic(board):
                    return True  # Si se resuelve, devuelve True

                board[row][col] = 0  # Si no se resuelve, retrocede y prueba otro número

        return False  # Si no se puede resolver el Sudoku, devuelve False

    # Función para encontrar la primera celda vacía
    def find_empty_location(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None, None

    # Función para verificar si un movimiento es válido
    def is_valid_move(board, row, col, num):
        # Verifica si el número ya está en la fila
        if num in board[row]:
            return False

        # Verifica si el número ya está en la columna
        if num in [board[i][col] for i in range(9)]:
            return False

        # Verifica si el número ya está en el cuadrado 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True
    
    inicio = time.time()
    
    if solve_sudoku_heuristic(sudoku):
        fin = time.time()
        tiempo = fin - inicio
        mostrar_solucion(sudoku, "Sudoku Resuelto - Avara", tiempo)
    else:
        print("\nNo se encontró solución para el Sudoku proporcionado.")
    


def mostrar_solucion(sudoku, titulo="Sudoku Resuelto", tiempo=None):
    ventana_solucion = tk.Tk()
    ventana_solucion.title(titulo)
    ventana_solucion.minsize(400, 400)  # Puedes ajustar esto según sea necesario
    tk.Label(ventana_solucion, text="Sudoku Resuelto", font=("Helvetica", 16, "bold")).pack(pady=(10, 20))

    # Marco para el Sudoku en el centro de la ventana
    marco_sudoku = tk.Frame(ventana_solucion)
    marco_sudoku.place(relx=0.5, rely=0.5, anchor="center")

    # Configurar la grilla para que las celdas del Sudoku se expandan
    for i in range(10):
        ventana_solucion.grid_rowconfigure(i, weight=1)
        ventana_solucion.grid_columnconfigure(i, weight=1)

    # Crear etiquetas para los números del Sudoku
    for i in range(9):
        for j in range(9):
            numero = sudoku[i][j] if sudoku[i][j] != 0 else ""
            celda = tk.Label(marco_sudoku, text=str(numero), width=2, height=1, borderwidth=1, relief="solid")
            celda.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

    # Etiqueta para el tiempo transcurrido
    if tiempo is not None:
        tiempo_label = tk.Label(ventana_solucion, text=f"Tiempo transcurrido: {tiempo:.2f} segundos")
        tiempo_label.place(relx=0.5, rely=0.97, anchor="s")

    ventana_solucion.mainloop()

   
