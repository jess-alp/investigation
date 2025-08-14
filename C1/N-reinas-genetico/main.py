import random
import time

n = 23

poblacion_tam = 100
generaciones = 10000000
tasa_mutacion = 0.05


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
        # Evaluar fitness
        poblacion.sort(key=fitness)
        if fitness(poblacion[0]) == 0:
            print(f"Solución encontrada en generación {generacion}")
            return poblacion[0]

        nueva_generacion = poblacion[:20]  # elitismo

        while len(nueva_generacion) < poblacion_tam:
            padres = random.sample(poblacion[:50], 2)
            hijo = cruzar(padres[0], padres[1])
            mutar(hijo)
            nueva_generacion.append(hijo)

        poblacion = nueva_generacion
    return None


inicio = time.time()
solucion = algoritmo_genetico()
fin = time.time()

if solucion:
    print("Solución:", solucion)
else:
    print("No se encontró solución en el límite de generaciones")

print(f"Tiempo total: {fin - inicio:.16f} segundos")