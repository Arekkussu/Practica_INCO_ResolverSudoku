import tkinter as tk
from tkinter import Label, messagebox
import random
import Profundidad
import Anchura
import Avara
import A_estrella
import copy

# El Sudoku inicial
sudoku_inicial = [
    [0, 0, 0, 4, 0, 0, 7, 0, 0],
    [8, 0, 7, 0, 0, 6, 0, 0, 0],
    [0, 6, 2, 0, 0, 0, 0, 1, 8],
    [0, 0, 0, 3, 0, 1, 8, 9, 0],
    [3, 0, 0, 6, 0, 0, 0, 4, 7],
    [0, 2, 0, 0, 0, 8, 0, 0, 0],
    [9, 0, 8, 0, 6, 3, 1, 5, 4],
    [2, 4, 3, 0, 7, 5, 6, 8, 0],
    [0, 1, 0, 0, 9, 4, 0, 0, 0]
]

def obtener_sudoku_inicial():
    return [fila[:] for fila in sudoku_inicial]

def generar_sudoku_aleatorio():
    return [[sudoku_inicial[i][j] if random.random() < 0.3 else 0 for j in range(9)] for i in range(9)]

def introducir_sudoku_gui():
    ventana_introducir = tk.Tk()
    ventana_introducir.title("Introducir Sudoku")
    ventana_introducir.minsize(300, 350)  # Ajusta el tamaño según sea necesario

    sudoku_temporal = [[0 for _ in range(9)] for _ in range(9)]
    celdas = [[None for _ in range(9)] for _ in range(9)]

    def on_celda_cambiada(i, j, event):
        valor = event.widget.get()
        if valor.isdigit() and 0 < int(valor) <= 9:
            sudoku_temporal[i][j] = int(valor)
        else:
            event.widget.delete(0, "end")

    def recoger_valores_sudoku():
        for i in range(9):
            for j in range(9):
                celda = celdas[i][j]
                valor = celda.get()
                if valor.isdigit() and 0 < int(valor) <= 9:
                    sudoku_temporal[i][j] = int(valor)
                else:
                    sudoku_temporal[i][j] = 0

    def confirmar():
        recoger_valores_sudoku()  # Asegúrate de recoger todos los valores antes de validar y cerrar
        if not es_sudoku_valido(sudoku_temporal):
            tk.messagebox.showerror("Error", "Sudoku incorrecto. Por favor, introduce un Sudoku válido.")
            ventana_introducir.destroy()  # Cierra la ventana actual
        else:
            ventana_introducir.destroy()  # Cierra la ventana de introducción
            mostrar_sudoku(sudoku_temporal)  # Muestra el sudoku introducido y el menú de algoritmos

    for i in range(9):
        for j in range(9):
            celda = tk.Entry(ventana_introducir, width=2, font=('Helvetica', 20), justify='center', borderwidth=2, relief="solid")
            celda.grid(row=i, column=j, padx=5, pady=5)
            celdas[i][j] = celda  # Almacena la referencia de la celda
            celda.bind("<FocusOut>", lambda event, i=i, j=j: on_celda_cambiada(i, j, event))

    tk.Button(ventana_introducir, text="Confirmar", command=confirmar).grid(row=9, column=0, columnspan=9, pady=20)

    ventana_introducir.mainloop()

def mostrar_sudoku(sudoku):
    if sudoku is None:
        print("ERROR: Error al retornar el sudoku.")
        return  # Termina la función si sudoku es None

    ventana_sudoku = tk.Tk()
    ventana_sudoku.title("Sudoku y Algoritmos")
    ventana_sudoku.minsize(400, 600)  # Ajusta el tamaño para dar espacio tanto al Sudoku como a los algoritmos

    # Marco para el Sudoku, colocado en la parte superior
    marco_sudoku = tk.Frame(ventana_sudoku)
    marco_sudoku.pack(side="top", pady=20)  # Usa pady para dar un poco de espacio alrededor del marco del Sudoku

    for i in range(9):
        for j in range(9):
            valor = sudoku[i][j]
            texto_celda = "" if valor == 0 else str(valor)
            Label(marco_sudoku, text=texto_celda, width=2, borderwidth=1, relief="solid").grid(row=i, column=j, padx=1, pady=1)  # Usa padx y pady para espaciar las celdas del Sudoku

    # Llama a la función para mostrar los botones de algoritmos, pasando el objeto ventana principal como parámetro
    mostrar_algoritmos(ventana_sudoku, sudoku)

    ventana_sudoku.mainloop()

def mostrar_algoritmos(ventana_principal, sudoku):
    # Hacer una copia profunda del Sudoku
    sudoku_copia = copy.deepcopy(sudoku)

    # Marco para los algoritmos, colocado debajo del marco del Sudoku
    algoritmos_frame = tk.Frame(ventana_principal)
    algoritmos_frame.pack(side="top", fill="x", pady=(20, 0))  # fill="x" hace que el marco se expanda horizontalmente
    # Botones para cada algoritmo
    tk.Button(algoritmos_frame, text="1. Profundidad", width=20,
              command=lambda: Profundidad.Profundidad(copy.deepcopy(sudoku_copia))).pack(pady=5, side="top")
    tk.Button(algoritmos_frame, text="2. Anchura", width=20, command=lambda: advertencia_anchura(copy.deepcopy(sudoku_copia))).pack(pady=5, side="top")
    tk.Button(algoritmos_frame, text="3. A*", width=20, command=lambda: A_estrella.A_estrella(copy.deepcopy(sudoku_copia))).pack(pady=5, side="top")
    tk.Button(algoritmos_frame, text="4. Coste", width=20).pack(pady=5, side="top")
    tk.Button(algoritmos_frame, text="5. Avara", width=20, command=lambda: Avara.avara(copy.deepcopy(sudoku_copia))).pack(pady=5, side="top")



# Funciones de Apoyo
def es_sudoku_valido(sudoku):
    for i in range(9):
        fila = set()
        columna = set()
        cuadrado = set()

        for j in range(9):
            # Comprobar la fila
            if sudoku[i][j] != 0 and sudoku[i][j] in fila:
                return False
            fila.add(sudoku[i][j])

            # Comprobar la columna
            if sudoku[j][i] != 0 and sudoku[j][i] in columna:
                return False
            columna.add(sudoku[j][i])

            # Comprobar el cuadrado 3x3
            cuadrante_fila = 3 * (i // 3)
            cuadrante_columna = 3 * (i % 3)
            valor_cuadrado = sudoku[cuadrante_fila + j // 3][cuadrante_columna + j % 3]
            if valor_cuadrado != 0 and valor_cuadrado in cuadrado:
                return False
            cuadrado.add(valor_cuadrado)

    return True

def advertencia_anchura(sudoku):
    respuesta = messagebox.askokcancel("Advertencia de eficiencia",
                                       "Este método no es eficiente y puede consumir muchos recursos.\n¿Deseas continuar?")
    if respuesta:
        # Aquí podrías llamar a la función del algoritmo de anchura o manejar la lógica deseada.
        print("Ejecutando algoritmo de anchura...")
        Anchura.Anchura(sudoku)
    else:
        print("Operación cancelada.")