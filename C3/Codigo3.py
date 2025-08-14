import random


n = 10
poblacion_size = 100
generaciones = 10000
tasa_mutacion = 0.05
contador_soluciones = 0
rango = (-5, 5)
desv = 0.1

def f(x1, x2):
    return x1**2 + x2**2

def fitness(ind):
    return 1 / (1 + f(ind[0], ind[1]))

def generar_poblacion():
    return [[random.uniform(*rango), random.uniform(*rango)] for _ in range(poblacion_size)]

def seleccionar_torneo(poblacion):
    torneo = random.sample(poblacion, 3)
    torneo.sort(key=lambda ind: fitness(ind), reverse=True)
    return torneo[0]

def crossover(p1, p2):
    alpha = random.random()
    hijo1 = [alpha*p1[0] + (1-alpha)*p2[0],
             alpha*p1[1] + (1-alpha)*p2[1]]
    hijo2 = [alpha*p2[0] + (1-alpha)*p1[0],
             alpha*p2[1] + (1-alpha)*p1[1]]
    return hijo1, hijo2

def mutar(ind):
    return [
        max(rango[0], min(rango[1], ind[0] + random.gauss(0, desv))),
        max(rango[0], min(rango[1], ind[1] + random.gauss(0, desv)))
    ]

def elitismo(poblacion, nueva_pob):
    mejor = max(poblacion, key=fitness)
    nueva_pob[random.randint(0, poblacion_size-1)] = mejor
    return nueva_pob

poblacion = generar_poblacion()

for gen in range(generaciones):
    mejor_ind = min(poblacion, key=lambda ind: f(ind[0], ind[1]))
    mejor_val = f(mejor_ind[0], mejor_ind[1])

    if mejor_val < 1e-6:
        contador_soluciones += 1

    nueva_pob = []
    while len(nueva_pob) < poblacion_size:
        p1 = seleccionar_torneo(poblacion)
        p2 = seleccionar_torneo(poblacion)
        hijo1, hijo2 = crossover(p1, p2)

        if random.random() < tasa_mutacion:
            hijo1 = mutar(hijo1)
        if random.random() < tasa_mutacion:
            hijo2 = mutar(hijo2)

        nueva_pob.append(hijo1)
        nueva_pob.append(hijo2)

    nueva_pob = elitismo(poblacion, nueva_pob)
    poblacion = nueva_pob

    if mejor_val == 0:
        break

mejor = min(poblacion, key=lambda ind: f(ind[0], ind[1]))
print("Mejor solución encontrada:", mejor)
print("Valor de la función:", f(mejor[0], mejor[1]))
print("Soluciones óptimas encontradas:", contador_soluciones)
