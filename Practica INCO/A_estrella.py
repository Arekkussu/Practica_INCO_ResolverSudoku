import heapq
import tkinter as tk
import time

def A_estrella(sudoku, mostrar=True):
    # Función para encontrar la primera celda vacía en el sudoku
    def encontrar_celda_vacia(sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    return i, j
        return None

    # Función para verificar si un número es válido en una celda específica
    def es_numero_valido(sudoku, fila, columna, numero):
        # Verificar si el número está presente en la fila
        if numero in sudoku[fila]:
            return False
        
        # Verificar si el número está presente en la columna
        if numero in [sudoku[i][columna] for i in range(9)]:
            return False
        
        # Verificar si el número está presente en el cuadrado 3x3
        fila_inicio, columna_inicio = 3 * (fila // 3), 3 * (columna // 3)
        for i in range(fila_inicio, fila_inicio + 3):
            for j in range(columna_inicio, columna_inicio + 3):
                if sudoku[i][j] == numero:
                    return False
        
        return True

    # Función para resolver el sudoku utilizando el algoritmo A*
    def resolver_sudoku_a_estrella(sudoku):
        # Definir la cola de prioridad para almacenar los estados del sudoku
        cola_prioridad = []
        
        # Añadir el sudoku inicial a la cola de prioridad con una prioridad de 0
        heapq.heappush(cola_prioridad, (0, sudoku))
        
        # Bucle principal de búsqueda A*
        while cola_prioridad:
            # Obtener el estado actual del sudoku y su prioridad
            _, estado_actual = heapq.heappop(cola_prioridad)
            
            # Encontrar la primera celda vacía en el sudoku
            celda_vacia = encontrar_celda_vacia(estado_actual)
            
            # Si no hay celdas vacías, el sudoku está resuelto
            if not celda_vacia:
                return estado_actual
            
            fila, columna = celda_vacia
            
            # Probar todos los números posibles en la celda vacía
            for numero in range(1, 10):
                # Verificar si el número es válido en la celda actual
                if es_numero_valido(estado_actual, fila, columna, numero):
                    # Crear una copia del estado actual del sudoku
                    nuevo_estado = [fila.copy() for fila in estado_actual]
                    
                    # Asignar el número válido a la celda vacía
                    nuevo_estado[fila][columna] = numero
                    
                    # Calcular la prioridad del nuevo estado (cantidad de celdas vacías restantes)
                    prioridad = sum(1 for i in range(9) for j in range(9) if nuevo_estado[i][j] == 0)
                    
                    # Añadir el nuevo estado a la cola de prioridad
                    heapq.heappush(cola_prioridad, (prioridad, nuevo_estado))

    inicio = time.time()
    
    if resolver_sudoku_a_estrella(sudoku):
        fin = time.time()
        tiempo = fin - inicio
        mostrar_solucion(sudoku, "Sudoku Resuelto - A*", tiempo)
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
