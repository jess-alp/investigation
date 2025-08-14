import time
inicio = time.time()

n = 14
contador = 0

#para marcar columnas y diágonales ocupadas
columna = [False] * n
diagonal_izquierda = [False] * (n * 2)
diagonal_derecha = [False] * (n * 2)

# coloca a una reina en cada fila
def backtrack(y, n, contador):
    #si se coloca una reina en cada fila es solución valida
    if (y == n):
        return contador + 1

    #intentamos poner una reina en casa columna de la fila
    for x in range(n):

        #variables para el estado de los datos
        global columna
        global diagonal_izquierda
        global diagonal_derecha

        if (columna[x] or diagonal_izquierda[x + y] or diagonal_derecha[x - y + n - 1]):
            continue
        # colocamos una reina
        columna[x] = diagonal_izquierda[x + y] = diagonal_derecha[x - y + n - 1] = True
        # enviamos la fila siguiente
        contador = backtrack(y + 1, n, contador)
        # quitamos la reina para probar otras posibilidades
        columna[x] = diagonal_izquierda[x + y] = diagonal_derecha[x - y + n - 1] = False

    return contador

#iniciamos la función y busqueda de soluciones
print(backtrack(0, n, contador))

#medimos el tiempo que tardo en encontrar la solución
fin = time.time()
print(f"Tiempo total: {fin - inicio:.4f} segundos")
