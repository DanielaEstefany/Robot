def buscar_queso(laberinto, raton_posicion, camino):
    # Obtenemos las dimensiones del laberinto
    filas = len(laberinto)
    columnas = len(laberinto[0])

    # Obtenemos las coordenadas del ratón
    raton_fila, raton_columna = raton_posicion

    # Verificamos si el ratón ha encontrado el queso
    if laberinto[raton_fila][raton_columna] == 'Q':
        print("¡El ratón ha encontrado el queso!")
        print("Camino: ", camino)
        return True

    # Verificamos si el ratón se encuentra en una posición válida
    if (
        raton_fila < 0 or raton_fila >= filas or
        raton_columna < 0 or raton_columna >= columnas or
        laberinto[raton_fila][raton_columna] == '#' or
        laberinto[raton_fila][raton_columna] == 'X'
    ):
        return False

    # Marcamos la posición actual del ratón como visitada
    laberinto[raton_fila][raton_columna] = 'X'

    # Exploramos las posibles direcciones en orden: arriba, derecha, abajo, izquierda
    if (
        buscar_queso(laberinto, (raton_fila - 1, raton_columna), camino + "U") or
        buscar_queso(laberinto, (raton_fila, raton_columna + 1), camino + "R") or
        buscar_queso(laberinto, (raton_fila + 1, raton_columna), camino + "D") or
        buscar_queso(laberinto, (raton_fila, raton_columna - 1), camino + "L")
    ):
        return True

    # Si ninguna dirección conduce al queso, retrocedemos
    laberinto[raton_fila][raton_columna] = '.'

    return False


# Ejemplo de uso
laberinto = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '.', '#', '.', '#', '#', '.', '#'],
    ['#', '.', '#', '.', '0', '.', '#', '.', '.', '#'],
    ['#', '.', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
]

raton_posicion_inicial = (3, 4)  # Posición inicial del ratón
camino_inicial = ""  # Camino inicial (vacío)
print(str(laberinto))
buscar_queso(laberinto, raton_posicion_inicial, camino_inicial)
print(str(laberinto))