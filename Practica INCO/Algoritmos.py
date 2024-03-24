import time
import tkinter as tk


def resolver_sudoku_profundidad(sudoku):
    for fila in range(9):
        for columna in range(9):
            if sudoku[fila][columna] == 0:
                for numero in range(1, 10):
                    # Verificar si el número es posible
                    if all(numero != sudoku[fila][j] for j in range(9)) and \
                            all(numero != sudoku[i][columna] for i in range(9)) and \
                            all(numero != sudoku[3 * (fila // 3) + i][3 * (columna // 3) + j] for i in range(3) for j in
                                range(3)):

                        sudoku[fila][columna] = numero

                        if resolver_sudoku_profundidad(sudoku):
                            return True

                        sudoku[fila][columna] = 0  # Backtrack
                return False
    return True  # Sudoku resuelto

def algoritmo_profundidad(sudoku):
    inicio = time.time()
    if resolver_sudoku_profundidad(sudoku):
        fin = time.time()
        tiempo = fin - inicio
        mostrar_solucion(sudoku, "Sudoku Resuelto - Profundidad", tiempo)
        print(f"Tiempo transcurrido: {tiempo:.2f} segundos")
    else:
        print("No se encontró una solución.")


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