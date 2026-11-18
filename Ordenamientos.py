import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import random
import time
import csv
import tracemalloc

# ==========================================
# 1. ALGORITMOS DE ORDENAMIENTO
# ==========================================

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izquierda = [x for x in arr if x < pivote]
    centro = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]
    return quick_sort(izquierda) + centro + quick_sort(derecha)

def heapify(arr, n, i):
    mayor = i
    izq = 2 * i + 1
    der = 2 * i + 2

    if izq < n and arr[izq] > arr[mayor]:
        mayor = izq
    if der < n and arr[der] > arr[mayor]:
        mayor = der

    if mayor != i:
        arr[i], arr[mayor] = arr[mayor], arr[i]
        heapify(arr, n, mayor)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def counting_sort_radix(arr, exp):
    n = len(arr)
    salida = [0] * n
    conteo = [0] * 10

    for i in range(n):
        indice = (arr[i] // exp) % 10
        conteo[indice] += 1

    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    i = n - 1
    while i >= 0:
        indice = (arr[i] // exp) % 10
        salida[conteo[indice] - 1] = arr[i]
        conteo[indice] -= 1
        i -= 1

    for i in range(n):
        arr[i] = salida[i]

def radix_sort_positivos(arr):
    if not arr:
        return arr
    maximo = max(arr)
    exp = 1
    while maximo // exp > 0:
        counting_sort_radix(arr, exp)
        exp *= 10
    return arr

def radix_sort(arr):
    negativos = [-x for x in arr if x < 0]
    positivos = [x for x in arr if x >= 0]
    
    negativos = radix_sort_positivos(negativos)
    positivos = radix_sort_positivos(positivos)
    
    return [-x for x in reversed(negativos)] + positivos

# ==========================================
# 2. INTERFAZ GRÁFICA CON TKINTER
# ==========================================

class AppOrdenamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos de Ordenamiento - Estándar")
        self.root.geometry("620x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        self.numeros = []
        self.ultimos_resultados = []

        # Título principal
        lbl_titulo = tk.Label(
            root, text="ANÁLISIS EMPÍRICO DE ORDENAMIENTO", 
            font=("Arial", 15, "bold"), bg="#f4f6f9", fg="#2c3e50"
        )
        lbl_titulo.pack(pady=12)

        # Sección 1: Cantidad y captura de números
        frame_captura = tk.Frame(root, bg="#f4f6f9")
        frame_captura.pack(pady=5)

        tk.Label(
            frame_captura, text="Cantidad:", 
            font=("Arial", 10, "bold"), bg="#f4f6f9"
        ).grid(row=0, column=0, padx=5)

        self.entry_cantidad = tk.Entry(frame_captura, width=8, font=("Arial", 11), justify="center")
        self.entry_cantidad.insert(0, "1000")
        self.entry_cantidad.grid(row=0, column=1, padx=5)

        btn_ingresar = tk.Button(
            frame_captura, text="Manual", font=("Arial", 9, "bold"),
            bg="#3498db", fg="white", command=self.pedir_numeros
        )
        btn_ingresar.grid(row=0, column=2, padx=3)

        btn_aleatorio = tk.Button(
            frame_captura, text="Aleatorio", font=("Arial", 9, "bold"),
            bg="#9b59b6", fg="white", command=self.generar_aleatorios
        )
        btn_aleatorio.grid(row=0, column=3, padx=3)

        # Sección de Escenarios de Prueba (Mejor / Peor Caso)
        frame_escenarios = tk.Frame(root, bg="#f4f6f9")
        frame_escenarios.pack(pady=5)

        btn_mejor = tk.Button(
            frame_escenarios, text="⭐ Mejor Caso (Ordenado)", font=("Arial", 9, "bold"),
            bg="#27ae60", fg="white", command=self.generar_mejor_caso
        )
        btn_mejor.grid(row=0, column=0, padx=5)

        btn_peor = tk.Button(
            frame_escenarios, text="⚠️ Peor Caso (Inverso)", font=("Arial", 9, "bold"),
            bg="#c0392b", fg="white", command=self.generar_peor_caso
        )
        btn_peor.grid(row=0, column=1, padx=5)

        # Etiqueta para mostrar la lista original
        self.lbl_original = tk.Label(
            root, text="Lista original: [ ]", font=("Arial", 9),
            bg="#ffffff", fg="#34495e", relief="solid", bd=1, width=72, height=3, wraplength=580
        )
        self.lbl_original.pack(pady=8)

        # Sección 2: Selección de método individual
        tk.Label(
            root, text="Selecciona un método individual:", 
            font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#2c3e50"
        ).pack(pady=3)

        frame_botones = tk.Frame(root, bg="#f4f6f9")
        frame_botones.pack(pady=3)

        metodos = [
            ("1. ShellSort", "ShellSort", 0, 0),
            ("2. QuickSort", "QuickSort", 0, 1),
            ("3. HeapSort", "HeapSort", 1, 0),
            ("4. RadixSort", "RadixSort", 1, 1)
        ]

        for texto, metodo, fila, col in metodos:
            btn = tk.Button(
                frame_botones, text=texto, font=("Arial", 10), width=22, height=2,
                bg="#1abc9c", fg="white", activebackground="#16a085",
                command=lambda m=metodo: self.ordenar(m)
            )
            btn.grid(row=fila, column=col, padx=8, pady=4)

        # Botón para comparar todos los métodos
        btn_comparar = tk.Button(
            root, text="Comparar Todos los Métodos (Benchmark + Memoria)", font=("Arial", 10, "bold"),
            bg="#f39c12", fg="white", activebackground="#d68910", width=50, height=2,
            command=self.comparar_todos
        )
        btn_comparar.pack(pady=6)

        # Etiqueta para mostrar el resultado
        self.lbl_resultado = tk.Label(
            root, text="Lista ordenada: [ ]", font=("Arial", 9, "bold"),
            bg="#ffffff", fg="#16a085", relief="solid", bd=1, width=72, height=3, wraplength=580
        )
        self.lbl_resultado.pack(pady=6)

        # Etiqueta para mostrar el tiempo y memoria individual
        self.lbl_tiempo = tk.Label(
            root, text="Rendimiento: -- ms | Memoria: -- KB", font=("Arial", 10, "bold"),
            bg="#f4f6f9", fg="#e67e22"
        )
        self.lbl_tiempo.pack(pady=3)

        # Botón Salir
        btn_salir = tk.Button(
            root, text="Salir del Programa", font=("Arial", 9, "bold"),
            bg="#7f8c8d", fg="white", width=20, command=self.salir
        )
        btn_salir.pack(pady=8)

    def obtener_cantidad(self):
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0:
                messagebox.showwarning("Atención", "Ingresa una cantidad mayor a 0.")
                return None
            return cantidad
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número entero válido.")
            return None

    def pedir_numeros(self):
        cantidad = self.obtener_cantidad()
        if cantidad is None:
            return

        nueva_lista = []
        for i in range(cantidad):
            num = simpledialog.askinteger(
                "Captura de datos", 
                f"Ingresa el número {i + 1} de {cantidad}:",
                parent=self.root
            )
            if num is None:
                return
            nueva_lista.append(num)
        self.actualizar_vista_datos(nueva_lista)

    def generar_aleatorios(self):
        cantidad = self.obtener_cantidad()
        if cantidad is None:
            return
        nueva_lista = [random.randint(-10000, 10000) for _ in range(cantidad)]
        self.actualizar_vista_datos(nueva_lista)

    def generar_mejor_caso(self):
        cantidad = self.obtener_cantidad()
        if cantidad is None:
            return
        nueva_lista = sorted([random.randint(-10000, 10000) for _ in range(cantidad)])
        self.actualizar_vista_datos(nueva_lista)

    def generar_peor_caso(self):
        cantidad = self.obtener_cantidad()
        if cantidad is None:
            return
        nueva_lista = sorted([random.randint(-10000, 10000) for _ in range(cantidad)], reverse=True)
        self.actualizar_vista_datos(nueva_lista)

    def actualizar_vista_datos(self, nueva_lista):
        self.numeros = nueva_lista
        texto_lista = self.formatear_lista(self.numeros)
        self.lbl_original.config(text=f"Lista original ({len(self.numeros)} elementos): {texto_lista}")
        self.lbl_resultado.config(text="Lista ordenada: [ ]")
        self.lbl_tiempo.config(text="Rendimiento: -- ms | Memoria: -- KB")

    def formatear_lista(self, lista):
        if len(lista) > 25:
            inicio = ", ".join(map(str, lista[:12]))
            fin = ", ".join(map(str, lista[-8:]))
            return f"[{inicio}, ... , {fin}]"
        return str(lista)

    def ejecutar_algoritmo(self, metodo, datos):
        copia = datos.copy()
        
        # Medición de memoria con tracemalloc (módulo nativo)
        tracemalloc.start()
        inicio = time.perf_counter()

        if metodo == "ShellSort":
            resultado = shell_sort(copia)
        elif metodo == "QuickSort":
            resultado = quick_sort(copia)
        elif metodo == "HeapSort":
            resultado = heap_sort(copia)
        elif metodo == "RadixSort":
            resultado = radix_sort(copia)

        fin = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tiempo_ms = (fin - inicio) * 1000
        memoria_kb = peak / 1024.0
        return resultado, tiempo_ms, memoria_kb

    def ordenar(self, metodo):
        if not self.numeros:
            messagebox.showwarning("Sin datos", "Primero ingresa o genera los números antes de ordenar.")
            return

        resultado, tiempo_ms, memoria_kb = self.ejecutar_algoritmo(metodo, self.numeros)

        texto_resultado = self.formatear_lista(resultado)
        self.lbl_resultado.config(text=f"Lista ordenada ({metodo}): {texto_resultado}")
        self.lbl_tiempo.config(text=f"Rendimiento ({metodo}): {tiempo_ms:.4f} ms | Memoria: {memoria_kb:.2f} KB")

    def comparar_todos(self):
        if not self.numeros:
            messagebox.showwarning("Sin datos", "Primero ingresa o genera los números para comparar.")
            return

        algoritmos = [
            ("ShellSort", "O(n log² n)"),
            ("QuickSort", "O(n log n)"),
            ("HeapSort", "O(n log n)"),
            ("RadixSort", "O(nk)")
        ]

        self.ultimos_resultados = []
        lista_ordenada_final = []

        for nombre, complejidad in algoritmos:
            res, tiempo, memoria = self.ejecutar_algoritmo(nombre, self.numeros)
            self.ultimos_resultados.append({
                "metodo": nombre,
                "tiempo": tiempo,
                "memoria": memoria,
                "complejidad": complejidad
            })
            lista_ordenada_final = res

        # Ordenar del más rápido al más lento
        self.ultimos_resultados.sort(key=lambda x: x["tiempo"])

        # Actualizar vista principal
        texto_resultado = self.formatear_lista(lista_ordenada_final)
        self.lbl_resultado.config(text=f"Lista ordenada (Benchmark): {texto_resultado}")
        mas_rapido = self.ultimos_resultados[0]
        self.lbl_tiempo.config(text=f"Más rápido: {mas_rapido['metodo']} ({mas_rapido['tiempo']:.4f} ms | {mas_rapido['memoria']:.2f} KB)")

        # Ventana emergente limpia con tabla y exportación a CSV
        self.mostrar_ventana_benchmark()

    def mostrar_ventana_benchmark(self):
        ventana_bench = tk.Toplevel(self.root)
        ventana_bench.title("Reporte de Benchmark y Memoria")
        ventana_bench.geometry("540x400")
        ventana_bench.configure(bg="#f4f6f9")
        ventana_bench.transient(self.root)
        ventana_bench.grab_set()

        tk.Label(
            ventana_bench, text=f"Resultados para {len(self.numeros)} elementos", 
            font=("Arial", 12, "bold"), bg="#f4f6f9", fg="#2c3e50"
        ).pack(pady=10)

        # Tabla (Treeview) ordenada por velocidad
        columnas = ("Metodo", "Tiempo (ms)", "Memoria (KB)", "Complejidad")
        tree = ttk.Treeview(ventana_bench, columns=columnas, show="headings", height=5)
        
        tree.heading("Metodo", text="Método")
        tree.heading("Tiempo (ms)", text="Tiempo (ms)")
        tree.heading("Memoria (KB)", text="Pico Memoria (KB)")
        tree.heading("Complejidad", text="Complejidad")

        tree.column("Metodo", width=110, anchor="center")
        tree.column("Tiempo (ms)", width=120, anchor="center")
        tree.column("Memoria (KB)", width=120, anchor="center")
        tree.column("Complejidad", width=130, anchor="center")

        for r in self.ultimos_resultados:
            tree.insert("", "end", values=(r["metodo"], f"{r['tiempo']:.4f} ms", f"{r['memoria']:.2f} KB", r["complejidad"]))

        tree.pack(pady=10)

        # Botones inferiores (Exportar CSV y Cerrar)
        frame_acciones = tk.Frame(ventana_bench, bg="#f4f6f9")
        frame_acciones.pack(pady=15)

        btn_csv = tk.Button(
            frame_acciones, text="💾 Exportar a CSV", font=("Arial", 10, "bold"),
            bg="#27ae60", fg="white", width=22, command=self.exportar_csv
        )
        btn_csv.grid(row=0, column=0, padx=10)

        btn_cerrar = tk.Button(
            frame_acciones, text="Cerrar", font=("Arial", 10, "bold"),
            bg="#34495e", fg="white", width=15, command=ventana_bench.destroy
        )
        btn_cerrar.grid(row=0, column=1, padx=10)

    def exportar_csv(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
            title="Guardar reporte CSV"
        )
        if not archivo:
            return

        try:
            with open(archivo, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Metodo", "Elementos", "Tiempo_ms", "Memoria_KB", "Complejidad"])
                for r in self.ultimos_resultados:
                    writer.writerow([r["metodo"], len(self.numeros), f"{r['tiempo']:.4f}", f"{r['memoria']:.2f}", r["complejidad"]])
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppOrdenamiento(root)
    root.mainloop()