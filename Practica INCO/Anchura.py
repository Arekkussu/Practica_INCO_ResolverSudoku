import time
import tkinter as tk

def Anchura(sudoku):
    def es_valido(s, num, pos):
        # Verificar la fila
        for i in range(9):
            if s[pos[0]][i] == num and pos[1] != i:
                return False

        # Verificar la columna
        for i in range(9):
            if s[i][pos[1]] == num and pos[0] != i:
                return False

        # Verificar el cuadrante
        cuadrante_x = pos[1] // 3
        cuadrante_y = pos[0] // 3

        for i in range(cuadrante_y * 3, cuadrante_y * 3 + 3):
            for j in range(cuadrante_x * 3, cuadrante_x * 3 + 3):
                if s[i][j] == num and (i,j) != pos:
                    return False

        return True

    def encontrar_siguiente_celda(s):
        for i in range(len(s)):
            for j in range(len(s[0])):
                if s[i][j] == 0:
                    return (i, j)  # fila, columna
        return None

    inicio = time.time()

    cola = [(sudoku, encontrar_siguiente_celda(sudoku))]

    while cola:
        actual, pos = cola.pop(0)  # Obtener el primer elemento de la cola

        if not pos:
            # No hay más celdas vacías, el sudoku está resuelto
            fin = time.time()
            mostrar_solucion(actual, "Sudoku Resuelto - Anchura", fin - inicio)
            return True

        fila, columna = pos

        for num in range(1, 10):
            if es_valido(actual, num, (fila, columna)):
                nuevo_sudoku = [fila[:] for fila in actual]
                nuevo_sudoku[fila][columna] = num
                nueva_pos = encontrar_siguiente_celda(nuevo_sudoku)

                cola.append((nuevo_sudoku, nueva_pos))

    print("No se encontró una solución.")
    return False

def mostrar_solucion(sudoku, titulo="Sudoku Resuelto", tiempo=None):
    ventana_solucion = tk.Tk()
    ventana_solucion.title(titulo)
    ventana_solucion.minsize(400, 400)

    tk.Label(ventana_solucion, text=titulo, font=("Helvetica", 16, "bold")).pack(pady=(10, 20))

    marco_sudoku = tk.Frame(ventana_solucion)
    marco_sudoku.pack(pady=20)

    for i in range(9):
        for j in range(9):
            numero = sudoku[i][j] if sudoku[i][j] != 0 else ""
            celda = tk.Label(marco_sudoku, text=str(numero), width=2, height=1, borderwidth=1, relief="solid")
            celda.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

    if tiempo is not None:
        tiempo_label = tk.Label(ventana_solucion, text=f"Tiempo transcurrido: {tiempo:.2f} segundos")
        tiempo_label.pack()

    ventana_solucion.mainloop()


