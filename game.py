import time
import pygame
import speech_recognition as sr
import sys
from collections import deque
import unicodedata

class Game:
    def __init__(self, window, width, height):
        # Configuración de la ventana y otras varables
        self.window = window
        self.width = width
        self.height = height

        # Resto de la inicialización del juego
        self.mapa = pygame.image.load("mapa1.png")  # Reemplaza "nombre_del_archivo.png" con el nombre de tu imagen de mapa
        self.mapa = pygame.transform.scale(self.mapa, (self.width, self.height))

        self.matrizG = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],    
        ['#', '#', '#', 'K', '#', '#', '#', '#', '#', '#', '#', 'N', 'N', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'R', '#', '#', '#'],
        ['#', '#', '#', 'K', '#', '#', '#', '#', '#', '#', '#', 'N', 'N', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'R', '#', '#', '#'],
        ['#', '1', '#', 'K', '#', '2', '#', '3', '#', '#', '4', 'N', 'N', '5', '#', '#', '6', '#', '7', '#', '#', '8', 'R', '#', '9', '#'],
        ['A', 'A', 'A','AK', 'A', 'A', 'A', 'A', 'A', 'A', 'A','AN','BN', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'BR','B', 'B', 'B'],
        ['#', '#', '#', 'K', '#', '#', '#', '#', '#', '#', '#', 'N', 'N', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'R', '#', '#', '#'],
        ['#', '#', '#', 'K', '#', '11', '#','12','#', '13','#', 'N', 'N', '#', '14','#', '15','#','16', '#', '17','#', 'R', '#', '18','#'],
        ['#','10', '#', 'K', '#', '#','CM', 'C', 'C', 'C', 'C','CN','DN', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D','DR', 'D','DS', 'D'],
        ['Z', 'Z', 'Z', 'K', '19','#', 'M', '#', '#', '#','#', 'N', 'N', '#', '21','#', '#', '#', '#', '#', '#', '#', '#', '#', 'S', 'S'],
        ['#', '#', '#', 'K ','#', '#', 'M', '#', '#', '#', '20', 'N', 'N', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'S', 'S'],
        ['#', '#', '#', 'K', '#', '#', 'M', '#', '#', '#', '#', 'N', 'N', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'S', 'S'],
        ['#', '22','#', 'K', '23','#', 'M', '24','#', '25','NE','N', 'N','NE', '#', '26','#','27', '#','28', '#', '#','29', '#', 'S', '#'],
        ['E', 'E', 'E','EK', 'E', 'E','EM', 'E', 'E', 'E', 'E', '30','#', 'E', 'F', 'F', 'F', 'F','FP', 'F', 'F', 'F', 'F', 'F','FS','31'],
        ['#', '#', '#', 'L', '#', '#', 'M', '#', '#', '#','OE', 'O', 'O','OE', '#', '#', '#', '#', 'P', '#', '#', 'Q', '#', '#', '#', ' '],
        ['#', '#', '#', 'L', '#', '#', 'M', '#', '#', '#', '#', 'O', 'O', '#', '#', '#', '#', '#', 'P', '#', '#', 'Q', '#', '#', '#', '#'],
        ['#', '#', '#', 'L', '#', '#', 'M', '#', '#', '#', '#', 'O', 'O', '#', '#', '#', '#', '#', 'P', '#', '#', 'Q', '#', '#', '#', '#'],
        ['#', '#', '32','L','33', '#', 'M', '#','34', '#','35', 'O', 'O', '#', '#', '#','36', '#', 'P','37', '#', 'Q','38', '#','39', '#'],
        ['G', 'G', 'G','GL', 'G', 'G','GM', 'G', 'G', 'G', 'G','GO','GO', 'V', 'V', 'V', 'V', 'V','HP', 'H', 'H','HQ', 'H', 'H', 'H', 'H'],
        ['#', '#', '#', 'L', '#', '#', 'M', '#', '#', '#', '#', 'O', 'O', '#', '#', '#', '#', '#', 'P', '#', '#', 'Q', '#', '#', '#', '#'],
        ['#', '40','#', 'L','41', '#', 'M', '#', '#','42', '#', 'O', 'O', '#','43', '#','44', '#', 'P', '#','45', 'Q', '#','46', '#','47'],
        ['I', 'I', 'I','IL', 'I', 'I','IM', 'I', 'I', 'I', 'I','IO','IO', 'V', 'V', 'V', 'V', 'V', 'P', 'J', 'J','JQ', 'J', 'J', 'J', 'J']
        ]

        self.block_width = self.width // 26
        self.block_height = self.height // 21

        self.robot_block = (14, 12)  # Bloque inicial del robot (fila, columna)
        self.school_block = (8, 2) # Bloque colegio
        self.circo_block = (20, 14) # Bloque circo
        self.calle1_block = (5, 4) # Bloque esquina(fila, columna)
        self.pizza_block = (7, 25) # Bloque pizza
        self.universidad_block = (17, 20) # Bloque universidad
        self.calle2_block = (5, 13) # Bloque inicial del robot (fila, columna)
        
        self.movement_requested = False

        self.recognizer = sr.Recognizer()

    def run(self):
        # Bucle principal del juego
        running = True
        while running:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        # Manejar eventos de teclado u otros eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar la tecla presionada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.robot_block = (max(1, self.robot_block[0] - 1), self.robot_block[1])
                    self.movement_requested = True
                elif event.key == pygame.K_DOWN:
                    self.robot_block = (min(21, self.robot_block[0] + 1), self.robot_block[1])
                    self.movement_requested = True
                elif event.key == pygame.K_LEFT:
                    self.robot_block = (self.robot_block[0], max(1, self.robot_block[1] - 1))
                    self.movement_requested = True
                elif event.key == pygame.K_RIGHT:
                    self.robot_block = (self.robot_block[0], min(26, self.robot_block[1] + 1))
                    self.movement_requested = True

    def update(self):
        # Utilizar el micrófono como fuente de audio
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, phrase_time_limit=8)

            try:
                # Reconocer el texto utilizando el reconocedor de voz
                text = self.recognizer.recognize_google(audio, language="es")

                # Imprimir el texto reconocido en la consola
                print("Texto reconocido:")
                print(text)

                # Procesar el texto reconocido
                self.process_text(text)

            except sr.UnknownValueError:
                print("No se pudo reconocer el audio.")

            except sr.RequestError as e:
                print("Error al solicitar los resultados del reconocimiento de voz; {0}".format(e))

        if self.movement_requested:
            pygame.time.wait(200)  # Pausa de 200 milisegundos entre cada movimiento del robot

    def render(self):
        imagen_robot = pygame.image.load("gordo.png")
        imagen_robot = pygame.transform.scale(imagen_robot, (self.block_width, self.block_height))  # Ajustar tamaño de la imagen al bloque
        # Limpiar la ventana con un color de fondo
        self.window.fill((255, 255, 255))

        # Dibujar el mapa en la ventana
        self.window.blit(self.mapa, (0, 0))

        # Dibujar lineas verticales para los bloques
        for col in range(1, 26):
            x = col * self.block_width
            pygame.draw.line(self.window, (0, 0, 0), (x, 0), (x, self.height))

        # Dibujar lineas horizontales para los bloques
        for row in range(1, 21):
            y = row * self.block_height
            pygame.draw.line(self.window, (0, 0, 0), (0, y), (self.width, y))

        # Dibujar el robot en la posición actual
        robot_x = (self.robot_block[1] - 1) * self.block_width
        robot_y = (self.robot_block[0] - 1) * self.block_height
        self.window.blit(imagen_robot, (robot_x, robot_y))

        # Actualizar la ventana
        pygame.display.flip()


    def quitar_tildes(self, texto):
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto

    def process_text(self, texto):
        text = self.quitar_tildes(texto)
        frase1 = "federico ve a"
        frase2 = "federico muevete a"
        frase3 = "federico dirigete a"
        frase4 = "federico conducete a"
        frase5 = "federico trasladate a"
        frase6 = "federico ve a esquina"
        frase7 = "federico muevete a esquina"
        frase8 = "federico dirigete a esquina"
        frase9 = "federico conducete a esquina"
        frase10 = "federico trasladate a esquina"
        frases = [frase1, frase2, frase3, frase4, frase5]
        frases1 = [frase6, frase7, frase8, frase9, frase10]

        for frase in frases:
            if frase in text.lower() and not "esquina" in text.lower():
                if "jugueteria" in text.lower():
                    self.movement_requested = "jugueteria"
                    self.move_robot_to_place("1")
                    break
                elif "lavandera" in text.lower():
                    self.movement_requested = "lavandera"
                    self.move_robot_to_place("2")
                    break
                elif "fruteria" in text.lower():
                    self.movement_requested = "fruteria"
                    self.move_robot_to_place("3")
                    break
                elif "supermercado" in text.lower():
                    self.movement_requested = "supermercado"
                    self.move_robot_to_place("4")
                    break
                elif "restaurante" in text.lower():
                    self.movement_requested = "restaurante"
                    self.move_robot_to_place("5")
                    break
                elif "panaderia" in text.lower():
                    self.movement_requested = "panaderia"
                    self.move_robot_to_place("6")
                    break
                elif "pescaderia" in text.lower():
                    self.movement_requested = "pescaderia"
                    self.move_robot_to_place("7")
                    break
                elif "veterinario" in text.lower():
                    self.movement_requested = "veterinario"
                    self.move_robot_to_place("8")
                    break
                elif "gasolinera" in text.lower():
                    self.movement_requested = "gasolinera"
                    self.move_robot_to_place("9")
                    break
                elif "escuela" in text.lower():
                    self.move_robot_to_place("10")
                    break
                elif "carniceria" in text.lower():
                    self.movement_requested = "carniceria"
                    self.move_robot_to_place("11")
                    break
                elif "tienda de instrumentos" in text.lower():
                    self.movement_requested = "tienda de instrumentos"
                    self.move_robot_to_place("12")
                    break
                elif "libreria" in text.lower():
                    self.movement_requested = "libreria"
                    self.move_robot_to_place("13")
                    break
                elif "sala de conciertos" in text.lower():
                    self.movement_requested = "sala de conciertos"
                    self.move_robot_to_place("14")
                    break

                elif "cine" in text.lower():
                    self.movement_requested = "cine"
                    self.move_robot_to_place("15")
                    break
                elif "quiosco" in text.lower():
                    self.movement_requested = "quiosco"
                    self.move_robot_to_place("16")
                    break
                elif "academia de idiomas" in text.lower():
                    self.movement_requested = "academia de idiomas"
                    self.move_robot_to_place("17")
                    break
                elif "pizzeria" in text.lower():
                    self.movement_requested = "pizzeria"
                    self.move_robot_to_place("18")
                    break
                elif "aparcamiento" in text.lower():
                    self.movement_requested = "aparcamiento"
                    self.move_robot_to_place("19")
                    break
                elif "iglesia" in text.lower():
                    self.movement_requested = "iglesia"
                    self.move_robot_to_place("20")
                    break
                elif "ayuntamiento" in text.lower():
                    self.movement_requested = "ayuntamiento"
                    self.move_robot_to_place("21")
                    break
                elif "cafeteria" in text.lower():
                    self.movement_requested = "cafeteria"
                    self.move_robot_to_place("22")
                    break
                elif "herboristeria" in text.lower():
                    self.movement_requested = "herboristeria"
                    self.move_robot_to_place("23")
                    break
                elif "correos" in text.lower():
                    self.movement_requested = "correos"
                    self.move_robot_to_place("24")
                    break
                elif "parada de autobús" in text.lower():
                    self.movement_requested = "parada de autobús"
                    self.move_robot_to_place("25")
                    break
                elif "banco" in text.lower():
                    self.movement_requested = "banco"
                    self.move_robot_to_place("26")
                    break
                elif "embajada" in text.lower():
                    self.movement_requested = "embajada"
                    self.move_robot_to_place("27")
                    break
                elif "hotel" in text.lower():
                    self.movement_requested = "hotel"
                    self.move_robot_to_place("28")
                    break
                elif "comisara de policia" in text.lower():
                    self.movement_requested = "comisara de policia"
                    self.move_robot_to_place("29")
                    break
                elif "plaza" in text.lower():
                    self.movement_requested = "plaza"
                    self.move_robot_to_place("30")
                    break
                elif "monumento nivel" in text.lower():
                    self.movement_requested = "monumento nivel"
                    self.move_robot_to_place("31")
                    break
                elif "estación de bomberos" in text.lower():
                    self.movement_requested = "estación de bomberos"
                    self.move_robot_to_place("32")
                    break
                elif "museo" in text.lower():
                    self.movement_requested = "museo"
                    self.move_robot_to_place("33")
                    break
                elif "hospital" in text.lower():
                    self.movement_requested = "hospital"
                    self.move_robot_to_place("34")
                    break
                elif "floristeria" in text.lower():
                    self.movement_requested = "floristeria"
                    self.move_robot_to_place("35")
                    break
                elif "biblioteca" in text.lower():
                    self.movement_requested = "biblioteca"
                    self.move_robot_to_place("36")
                    break
                elif "universidad" in text.lower():
                    self.movement_requested = "universidad"
                    self.move_robot_to_place("37")
                    break
                elif "bar" in text.lower():
                    self.movement_requested = "bar"
                    self.move_robot_to_place("38")
                    break
                elif "estación de tren" in text.lower():
                    self.movement_requested = "estación de tren"
                    self.move_robot_to_place("39")
                    break
                elif "peluqueria" in text.lower():
                    self.movement_requested = "peluqueria"
                    self.move_robot_to_place("40")
                    break
                elif "centro comercial" in text.lower():
                    self.movement_requested = "centro comercial"
                    self.move_robot_to_place("41")
                    break
                elif "farmacia" in text.lower():
                    self.movement_requested = "farmacia"
                    self.move_robot_to_place("42")
                    break
                elif "circo" in text.lower():
                    self.movement_requested = "circo"
                    self.move_robot_to_place("43")
                    break
                elif "teatro" in text.lower():
                    self.movement_requested = "teatro"
                    self.move_robot_to_place("44")
                    break
                elif "tienda de ropa" in text.lower():
                    self.movement_requested = "tienda de ropa"
                    self.move_robot_to_place("45")
                    break
                elif "casa de pepe" in text.lower():
                    self.movement_requested = "casa de pepe"
                    self.move_robot_to_place("46")
                    break
                elif "ambulatorio" in text.lower():
                    self.movement_requested = "ambulatorio"
                    self.move_robot_to_place("47")
                    break
                elif "calle profe inolvidable" in text.lower():
                    self.movement_requested = "calle profe inolvidable"
                    self.move_robot_to_place("A")
                    break
                elif "calle del vocabulario" in text.lower():
                    self.movement_requested = "calle del vocabulario"
                    self.move_robot_to_place("B")
                    break
                elif "calle del ser y estar" in text.lower():
                    self.movement_requested = "calle del ser y estar"
                    self.move_robot_to_place("C")
                    break
                elif "calle del instituto cervantes" in text.lower():
                    self.movement_requested = "calle del instituto cervantes"
                    self.move_robot_to_place("D")
                    break
                elif "avenida hablo español" in text.lower():
                    self.movement_requested = "avenida hablo español"
                    self.move_robot_to_place("E")
                    break
                elif "avenida profe de ele" in text.lower():
                    self.movement_requested = "avenida profe de ele"
                    self.move_robot_to_place("F")
                    break
                elif "calle del sustantivo" in text.lower():
                    self.movement_requested = "calle del sustantivo"
                    self.move_robot_to_place("G")
                    break
                elif "calle del me gusta" in text.lower():
                    self.movement_requested = "calle del me gusta"
                    self.move_robot_to_place("H")
                    break
                elif "calle de los errores" in text.lower():
                    self.movement_requested = "calle de los errores"
                    self.move_robot_to_place("I")
                    break
                elif "calle de por y para" in text.lower():
                    self.movement_requested = "calle de por y para"
                    self.move_robot_to_place("J")
                    breakpoint
                elif "calle del adjetivo" in text.lower():
                    self.movement_requested = "calle del adjetivo"
                    self.move_robot_to_place("K")
                    break
                elif "calle del siele" in text.lower():
                    self.movement_requested = "calle del siele"
                    self.move_robot_to_place("L")
                    break
                elif "calle de los deberes hechos" in text.lower():
                    self.movement_requested = "calle de los deberes hechos"
                    self.move_robot_to_place("M")
                    break
                elif "avenida del subjuntivo" in text.lower():
                    self.movement_requested = "avenida del subjuntivo"
                    self.move_robot_to_place("N")
                    break
                elif "avenida del indicativo" in text.lower():
                    self.movement_requested = "avenida del indicativo"
                    self.move_robot_to_place("O")
                    break
                elif "calle de los verbos" in text.lower():
                    self.movement_requested = "calle de los verbos"
                    self.move_robot_to_place("P")
                    break
                elif "calle de la gramatica" in text.lower():
                    self.movement_requested = "calle de la gramatica"
                    self.move_robot_to_place("Q")
                    break
                elif "calle de las dudas" in text.lower():
                    self.movement_requested = "calle de las dudas"
                    self.move_robot_to_place("R")
                    break
                elif "calle de la n" in text.lower():
                    self.movement_requested = "calle de la n"
                    self.move_robot_to_place("S")
                    break  
                elif "parque ele" in text.lower():
                    self.movement_requested = "parque ele"
                    self.move_robot_to_place("V")
                    break
                elif " " in text.lower():
                    print("no conozco ese lugar")

        else:
            for frase in frases1:
                if frase in text.lower():
                    if "adjetivo" and "inolvidable"  in text.lower():
                        self.movement_requested = "calle del adjetivo esquina calle profe inolvidable"
                        self.move_robot_to_place('AK') 
                else:
                    print("no se hacer eso")
        

    def crearMatriz(self, x, y):
        matriz = []

        # Crear filas
        for i in range(21):
            fila = []
            # Crear columnas
            for j in range(26):
                fila.append('.')  # Agregar elementos vacios a la fila
            matriz.append(fila)  # Agregar fila a la matriz
        matriz[x][y] = 'Q'
        return matriz
    
    def move_robot_to_place(self, place):
        # Calcular la dirección del movimiento hacia la escuela
        robotPos = (self.robot_block[0]-1,self.robot_block[1]-1)
        caminoPos = [(self.robot_block[0]-1,self.robot_block[1]-1)]
        camino = self.buscar_queso(self.matrizG, robotPos, caminoPos, place)
        print(str(camino))
        for coordenada in camino:
            next_block = (coordenada[0] + 1, coordenada[1] + 1)
            self.robot_block = next_block

            time.sleep(1)
            self.render()

    """def move_robot_to_school(self):
        # Calcular la dirección del movimiento hacia la escuela
        school = '10'
        robotPos = (self.robot_block[0]-1,self.robot_block[1]-1)
        caminoPos = [(self.robot_block[0]-1,self.robot_block[1]-1)]
        camino = self.buscar_queso(self.matrizG, robotPos, caminoPos, school)
        print(str(camino))
        for coordenada in camino:
            next_block = (coordenada[0] + 1, coordenada[1] + 1)
            self.robot_block = next_block

            time.sleep(1)
            self.render()

    def is_block_valid(self, block):
        if block in self.blocked_blocks:
            return False
        return True"""
        
    def buscar_queso(self, laberinto, raton_posicion, camino, destino):

        filas = len(laberinto)
        columnas = len(laberinto[0])

        raton_fila, raton_columna = raton_posicion

        visitados = set()
        visitados.add((raton_fila, raton_columna))

        queue = deque([(raton_fila, raton_columna, [])])

        while queue:
            fila, columna, camino = queue.popleft()

            if laberinto[fila][columna] == destino:
                return camino

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nueva_fila = fila + dx
                nueva_columna = columna + dy

                if (
                    nueva_fila >= 0 and nueva_fila < filas and
                    nueva_columna >= 0 and nueva_columna < columnas and
                    laberinto[nueva_fila][nueva_columna] != '#' and
                    (nueva_fila, nueva_columna) not in visitados
                ):
                    visitados.add((nueva_fila, nueva_columna))
                    queue.append((nueva_fila, nueva_columna, camino + [(nueva_fila, nueva_columna)]))

        return None

    


