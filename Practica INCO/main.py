import tkinter as tk


import GenerarSudoku  # Importamos el módulo GenerarSudoku

def inicial():
    global sudoku_actual
    sudoku_actual = GenerarSudoku.obtener_sudoku_inicial()
    GenerarSudoku.mostrar_sudoku(sudoku_actual)

def generado():
    global sudoku_actual
    sudoku_actual = GenerarSudoku.generar_sudoku_aleatorio()
    GenerarSudoku.mostrar_sudoku(sudoku_actual)

def introducir():
    global sudoku_actual
    sudoku_actual = GenerarSudoku.introducir_sudoku_gui()
    GenerarSudoku.mostrar_sudoku(sudoku_actual)

# TODO: CUANDO SE CIERRA LA VENTANA DEL MENU PRINCIPAL SALTA UNA EXCEPCIÓN

def mostrar_menu():
    root = tk.Tk()
    root.title("Sudoku Solver")
    root.minsize(400, 400)

    tk.Label(root, text="SUDOKU", font=("Helvetica", 20, "bold")).pack(pady=(10, 20))

    tk.Button(root, text="1- Sudoku Inicial", width=20, command=inicial).pack(pady=5)
    tk.Button(root, text="2- Generar Sudoku", width=20, command=generado).pack(pady=5)
    tk.Button(root, text="3- Introducir por pantalla", width=20, command=introducir).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    mostrar_menu()