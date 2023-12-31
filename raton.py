def buscar_queso(laberinto, raton_posicion, camino):
    # Obtenemos las dimensiones del laberinto
    filas = len(laberinto)
    columnas = len(laberinto[0])

    # Obtenemos las coordenadas del ratón
    raton_fila, raton_columna = raton_posicion
    if raton_fila < 0 or raton_fila >= filas or raton_columna < 0 or raton_columna >= columnas:      
        return None 

    # Verificamos si el ratón ha encontrado el queso
    if laberinto[raton_fila][raton_columna] == 'Q':
        return camino

    # Verificamos si el ratón se encuentra en una posición válida
    if (
        laberinto[raton_fila][raton_columna] == '#' or
        laberinto[raton_fila][raton_columna] == 'X'
    ):
        return None

    # Marcamos la posición actual del ratón como visitada
    laberinto[raton_fila][raton_columna] = 'X'

    # Exploramos las posibles direcciones en orden: arriba, derecha, abajo, izquierda
    camino_actual = None

    if not camino_actual:
        camino_actual = buscar_queso(laberinto, (raton_fila - 1, raton_columna), camino + [(raton_fila - 1, raton_columna)])  # Arriba

    if not camino_actual:
        camino_actual = buscar_queso(laberinto, (raton_fila, raton_columna + 1), camino + [(raton_fila, raton_columna + 1)])  # Derecha

    if not camino_actual:
        camino_actual = buscar_queso(laberinto, (raton_fila + 1, raton_columna), camino + [(raton_fila + 1, raton_columna)])  # Abajo

    if not camino_actual:
        camino_actual = buscar_queso(laberinto, (raton_fila, raton_columna - 1), camino + [(raton_fila, raton_columna - 1)])  # Izquierda

    # Si ninguna dirección conduce al queso, retrocedemos
    laberinto[raton_fila][raton_columna] = '.'

    return camino_actual

# Ejemplo de uso
laberinto = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', '#', ' ', '#', '#', ' ', ' ', '#', ' ', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
        ['#', 'Q', '#', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', ' ', '#', ' ', '#', '#', '#', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]
 
camino = buscar_queso(laberinto, (13, 11), [(13, 11)])
print(str(camino))