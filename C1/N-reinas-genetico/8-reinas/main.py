import random
import time
import tkinter as tk

n = 8
poblacion_tam = 100
generaciones = 1000000
tasa_mutacion = 0.05
contador_soluciones = 0


def fitness(tablero):
    conflictos = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1
    return conflictos


def crear_individuo():
    individuo = list(range(n))
    random.shuffle(individuo)
    return individuo


def cruzar(padre1, padre2):
    a, b = sorted(random.sample(range(n), 2))
    hijo = [None] * n
    hijo[a:b] = padre1[a:b]
    restantes = [gen for gen in padre2 if gen not in hijo]
    k = 0
    for i in range(n):
        if hijo[i] is None:
            hijo[i] = restantes[k]
            k += 1
    return hijo



def mutar(individuo):
    if random.random() < tasa_mutacion:
        i, j = random.sample(range(n), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]



def algoritmo_genetico():
    poblacion = [crear_individuo() for _ in range(poblacion_tam)]
    for generacion in range(generaciones):
        poblacion.sort(key=fitness)
        if fitness(poblacion[0]) == 0:
            return poblacion[0], generacion
        nueva_gen = poblacion[:20]
        while len(nueva_gen) < poblacion_tam:
            p1, p2 = random.sample(poblacion[:50], 2)
            hijo = cruzar(p1, p2)
            mutar(hijo)
            nueva_gen.append(hijo)
        poblacion = nueva_gen
    return None, generaciones


def dibujar_tablero(solucion, generacion):
    canvas.delete("all")
    size = min(600 // n, 60)
    canvas.config(width=n * size, height=n * size)

    for i in range(n):
        for j in range(n):
            color = "#F0D9B5" if (i + j) % 2 == 0 else "#B58863"
            canvas.create_rectangle(j * size, i * size, (j + 1) * size, (i + 1) * size, fill=color, outline="black")

    for fila, col in enumerate(solucion):
        x = col * size + size // 2
        y = fila * size + size // 2
        canvas.create_oval(x - size // 3, y - size // 3, x + size // 3, y + size // 3, fill="red")


def buscar_y_mostrar():
    global contador_soluciones
    inicio = time.time()
    solucion, gen = algoritmo_genetico()
    fin = time.time()

    if solucion:
        contador_soluciones += 1
        dibujar_tablero(solucion, gen)
        etiqueta_info.config(text=f"Generación: {gen}     Tiempo: {fin - inicio:.3f} s")
        etiqueta_contador.config(text=f"Soluciones encontradas: {contador_soluciones}")
    else:
        etiqueta_info.config(text="No se encontró solución.")


# === Interfaz gráfica ===
ventana = tk.Tk()
ventana.title("N Reinas - Algoritmo Genético")

# Canvas para tablero
canvas = tk.Canvas(ventana)
canvas.pack()

# Etiquetas y botones
etiqueta_info = tk.Label(ventana, text="", font=("Arial", 10))
etiqueta_info.pack()

etiqueta_contador = tk.Label(ventana, text="Soluciones encontradas: 0", font=("Arial", 11, "bold"))
etiqueta_contador.pack()

boton_buscar = tk.Button(ventana, text="Buscar nueva solución", command=buscar_y_mostrar)
boton_buscar.pack(pady=5)



frame_n = tk.Frame(ventana)
frame_n.pack(pady=10)

tk.Label(frame_n, text="Cambiar N:").pack(side="left")

entrada_n = tk.Entry(frame_n, width=5)
entrada_n.insert(0, str(n))
entrada_n.pack(side="left")


def cambiar_n():
    global n, contador_soluciones
    try:
        nuevo_n = int(entrada_n.get())
        if nuevo_n < 4 or nuevo_n > 50:
            raise ValueError
        n = nuevo_n
        contador_soluciones = 0
        etiqueta_contador.config(text="Soluciones encontradas: 0")
        buscar_y_mostrar()
    except ValueError:
        etiqueta_info.config(text="Ingresa un valor entre 4 y 50")


boton_cambiar_n = tk.Button(frame_n, text="Aplicar", command=cambiar_n)
boton_cambiar_n.pack(side="left", padx=5)

buscar_y_mostrar()
ventana.mainloop()