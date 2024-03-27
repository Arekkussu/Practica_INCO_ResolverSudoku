import time
import tkinter as tk


def Profundidad(sudoku, mostrar=True):
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

        for i in range(cuadrante_y*3, cuadrante_y*3 + 3):
            for j in range(cuadrante_x * 3, cuadrante_x*3 + 3):
                if s[i][j] == num and (i, j) != pos:
                    return False
        return True
    def encontrar_vacia(s):
        for i in range(len(s)):
            for j in range(len(s[0])):
                if s[i][j] == 0:
                    return (i, j)  # fila, columna
        return None
    def resolver(s):
        encontrar = encontrar_vacia(s)
        if not encontrar:
            return True  # Solucionado
        else:
            fila, columna = encontrar

        for i in range(1, 10):
            if es_valido(s, i, (fila, columna)):
                s[fila][columna] = i

                if resolver(s):
                    return True

                s[fila][columna] = 0  # Backtrack

        return False  # Sin solucion
    
    inicio = time.time()

    if resolver(sudoku):
        fin = time.time()
        tiempo = fin - inicio

        if mostrar:
            mostrar_solucion(sudoku, "Sudoku Resuelto - Profundidad", tiempo)
        print(f"Tiempo transcurrido: {tiempo:.2f} segundos")
        return True  # Sudoku resuelto
    else:
        print("No se encontró una solución.")
        return False  # Sin solución

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