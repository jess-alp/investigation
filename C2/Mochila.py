import random

valores = []
pesos = []

with open("ks_30_0.txt", "r") as f:
    for linea in f:
        partes = linea.strip().split()
        if len(partes) != 2:
            continue
        try:
            v, p = map(int, partes)
        except ValueError:
            continue
        valores.append(v)
        pesos.append(p)

capacidad = 1000000
poblacion_tam = 20
generaciones = 1000
tasa_mutacion = 0.1

def fitness(individuo):
    valor_total = 0
    peso_total = 0
    for i in range(len(individuo)):
        if individuo[i] == 1:
            valor_total += valores[i]
            peso_total += pesos[i]
    if peso_total > capacidad:
        return 0
    return valor_total

def crear_individuo():
    return [random.randint(0, 1) for _ in range(len(valores))]

def seleccion(poblacion):
    pesos_fitness = [fitness(ind) for ind in poblacion]
    if sum(pesos_fitness) == 0:
        return random.sample(poblacion, 2)
    return random.choices(poblacion, weights=pesos_fitness, k=2)

def cruce(padre1, padre2):
    punto = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2

def mutacion(individuo):
    for i in range(len(individuo)):
        if random.random() < tasa_mutacion:
            individuo[i] = 1 - individuo[i]

poblacion = [crear_individuo() for _ in range(poblacion_tam)]

for generacion in range(generaciones):
    nueva_poblacion = []
    for _ in range(poblacion_tam // 2):
        padre1, padre2 = seleccion(poblacion)
        hijo1, hijo2 = cruce(padre1, padre2)
        mutacion(hijo1)
        mutacion(hijo2)
        nueva_poblacion.extend([hijo1, hijo2])
    poblacion = nueva_poblacion

mejor = max(poblacion, key=fitness)
print("Mejor individuo:", mejor)
print("Valor total:", fitness(mejor))
print("Peso total:", sum(pesos[i] for i in range(len(mejor)) if mejor[i] == 1))


