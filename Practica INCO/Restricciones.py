import tkinter as tk
import time

def restricciones(sudoku_generado, mostrar=True):
    def encontrar_celda_vacia(tablero):
        # Encuentra la siguiente celda vacía en el tablero
        for fila in range(9):
            for columna in range(9):
                if tablero[fila][columna] == 0:
                    return fila, columna
        return None, None  # Retorna None si no hay celdas vacías

    def es_valido(tablero, fila, columna, num):
        # Verifica si es válido colocar 'num' en la posición (fila, columna)
        # Verifica si 'num' no está presente en la misma fila o columna
        for i in range(9):
            if tablero[fila][i] == num or tablero[i][columna] == num:
                return False
        # Verifica si 'num' no está presente en el mismo cuadrante 3x3
        inicio_fila, inicio_columna = 3 * (fila // 3), 3 * (columna // 3)
        for i in range(3):
            for j in range(3):
                if tablero[inicio_fila + i][inicio_columna + j] == num:
                    return False
        return True

    def encontrar_posibilidades(tablero, fila, columna):
        # Encuentra los números posibles para la celda (fila, columna) del tablero
        posibilidades = set(range(1, 10))
        for i in range(9):
            if tablero[fila][i] != 0:
                posibilidades.discard(tablero[fila][i])
            if tablero[i][columna] != 0:
                posibilidades.discard(tablero[i][columna])
        inicio_fila, inicio_columna = 3 * (fila // 3), 3 * (columna // 3)
        for i in range(3):
            for j in range(3):
                if tablero[inicio_fila + i][inicio_columna + j] != 0:
                    posibilidades.discard(tablero[inicio_fila + i][inicio_columna + j])
        return posibilidades

    def resolver_sudoku(tablero):
        fila, columna = encontrar_celda_vacia(tablero)
        if fila is None:  # Si no hay celdas vacías, el sudoku está resuelto
            return True
        posibilidades = encontrar_posibilidades(tablero, fila, columna)
        if not posibilidades:
            return False  # Si no hay posibilidades para la celda, retrocede

        for num in posibilidades:
            if es_valido(tablero, fila, columna, num):
                tablero[fila][columna] = num  # Asigna un número válido
                if resolver_sudoku(tablero):
                    return True
                tablero[fila][columna] = 0  # Si no se puede resolver, retrocede
        return False

    inicio = time.time()
    
    if resolver_sudoku(sudoku_generado):
        fin = time.time()
        tiempo = fin - inicio
        mostrar_solucion(sudoku_generado, "Sudoku Resuelto - Restricciones", tiempo)
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

