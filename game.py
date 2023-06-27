import time
import pygame
import speech_recognition as sr
import sys
from collections import deque

class Game:
    def __init__(self, window, width, height):
        # Configuración de la ventana y otras variables
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
        ['Z', 'Z', 'Z', 'K', '19','#', 'M', '#', '#', '20','#', 'N', 'N', '#', '21','#', '#', '#', '#', '#', '#', '#', '#', '#', 'S', 'S'],
        ['#', '#', '#', 'K ','#', '#', 'M', '#', '#', '#', '#', 'N', 'N', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'S', 'S'],
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
            if self.movement_requested == "escuela":
                self.move_robot_to_school()
            elif self.movement_requested == "universidad":
                self.move_robot_to_university()
            elif self.movement_requested == "circo":
                self.move_robot_to_circo()
            elif self.movement_requested == "calle 1":
                self.move_robot_to_calle1()
            elif self.movement_requested == "calle 2":
                self.move_robot_to_calle2()
            elif self.movement_requested == "pizza":
                self.move_robot_to_pizza()
            pygame.time.wait(200)  # Pausa de 200 milisegundos entre cada movimiento del robot

    def render(self):
        imagen_robot = pygame.image.load("gordo.png")
        imagen_robot = pygame.transform.scale(imagen_robot, (self.block_width, self.block_height))  # Ajustar tamaño de la imagen al bloque
        # Limpiar la ventana con un color de fondo
        self.window.fill((255, 255, 255))

        # Dibujar el mapa en la ventana
        self.window.blit(self.mapa, (0, 0))

        # Dibujar líneas verticales para los bloques
        for col in range(1, 26):
            x = col * self.block_width
            pygame.draw.line(self.window, (0, 0, 0), (x, 0), (x, self.height))

        # Dibujar líneas horizontales para los bloques
        for row in range(1, 21):
            y = row * self.block_height
            pygame.draw.line(self.window, (0, 0, 0), (0, y), (self.width, y))

        # Dibujar el robot en la posición actual
        robot_x = (self.robot_block[1] - 1) * self.block_width
        robot_y = (self.robot_block[0] - 1) * self.block_height
        self.window.blit(imagen_robot, (robot_x, robot_y))

        # Actualizar la ventana
        pygame.display.flip()

    def process_text(self, text):

        frase1 = "gordo ve a"
        frase2 = "gordo muevete a"
        frase3 = "gordo dirigete a"
        frase4 = "gordo conduce a"
        frase5 = "gordo trasladate a"
        frases = [frase1, frase2, frase3, frase4, frase5]

        for frase in frases:
            if frase in text.lower():
                if "jugueteria" in text.lower():
                    self.movement_requested = "jugueteria"
                    break
                elif "lavanderia" in text.lower():
                    self.movement_requested = "lavanderia"
                    break
                elif "fruteria" in text.lower():
                    self.movement_requested = "fruteria"
                    break
                elif "supermercado" in text.lower():
                    self.movement_requested = "supermercado"
                    break
                elif "restaurante" in text.lower():
                    self.movement_requested = "restaurante"
                    break
                elif "pescadería" in text.lower():
                    self.movement_requested = "pescadería"
                    break
                elif "veterinario" in text.lower():
                    self.movement_requested = "veterinario"
                    break
                elif "gasolinera" in text.lower():
                    self.movement_requested = "gasolinera"
                    break
                elif "escuela" in text.lower():
                    self.movement_requested = "escuela"
                    break
                elif "carnicería" in text.lower():
                    self.movement_requested = "carnicería"
                    break
                elif "tienda de instrumentos" in text.lower():
                    self.movement_requested = "tienda de instrumentos"
                    break
                elif "librería" in text.lower():
                    self.movement_requested = "librería"
                    break
                elif "sala de conciertos" in text.lower():
                    self.movement_requested = "sala de conciertos"
                    break

                elif "cine" in text.lower():
                    self.movement_requested = "cine"
                    break
                elif "quiosco" in text.lower():
                    self.movement_requested = "quiosco"
                    break
                elif "academia de idiomas" in text.lower():
                    self.movement_requested = "academia de idiomas"
                    break
                elif "pizzería" in text.lower():
                    self.movement_requested = "pizzería"
                    break
                elif "aparcamiento" in text.lower():
                    self.movement_requested = "aparcamiento"
                    break
                elif "iglesia" in text.lower():
                    self.movement_requested = "iglesia"
                    break
                elif "ayuntamiento" in text.lower():
                    self.movement_requested = "ayuntamiento"
                    break
                elif "cafetería" in text.lower():
                    self.movement_requested = "cafetería"
                    break
                elif "herboristería" in text.lower():
                    self.movement_requested = "herboristería"
                    break
                elif "correos" in text.lower():
                    self.movement_requested = "correos"
                    break
                elif "parada de autobús" in text.lower():
                    self.movement_requested = "parada de autobús"
                    break
                elif "banco" in text.lower():
                    self.movement_requested = "banco"
                    break
                elif "embajada" in text.lower():
                    self.movement_requested = "embajada"
                    break
                elif "hotel" in text.lower():
                    self.movement_requested = "hotel"
                    break
                elif "comisaria de policía" in text.lower():
                    self.movement_requested = "comisaria de policía"
                    break
                elif "plaza" in text.lower():
                    self.movement_requested = "plaza"
                    break
                elif "monumento nivel" in text.lower():
                    self.movement_requested = "monumento nivel"
                    break
                elif "estación de bomberos" in text.lower():
                    self.movement_requested = "estación de bomberos"
                    break
                elif "museo" in text.lower():
                    self.movement_requested = "museo"
                    break
                elif "hospital" in text.lower():
                    self.movement_requested = "hospital"
                    break
                elif "floristería" in text.lower():
                    self.movement_requested = "floristería"
                    break
                elif "biblioteca" in text.lower():
                    self.movement_requested = "biblioteca"
                    break
                elif "universidad" in text.lower():
                    self.movement_requested = "universidad"
                    break
                elif "bar" in text.lower():
                    self.movement_requested = "bar"
                    break
                elif "estación de tren" in text.lower():
                    self.movement_requested = "estación de tren"
                    break
                elif "peluquería" in text.lower():
                    self.movement_requested = "peluquería"
                    break
                elif "centro comercial" in text.lower():
                    self.movement_requested = "centro comercial"
                    break
                elif "farmacia" in text.lower():
                    self.movement_requested = "farmacia"
                    break
                elif "circo" in text.lower():
                    self.movement_requested = "circo"
                    break
                elif "teatro" in text.lower():
                    self.movement_requested = "teatro"
                    break
                elif "tienda de ropa" in text.lower():
                    self.movement_requested = "tienda de ropa"
                    break
                elif "casa de pepe" in text.lower():
                    self.movement_requested = "casa de pepe"
                    break
                elif "ambulatorio" in text.lower():
                    self.movement_requested = "ambulatorio"
                    break
                elif "calle profe inolvidable" in text.lower():
                    self.movement_requested = "calle profe inolvidable"
                    break
                elif "calle del vocabulario" in text.lower():
                    self.movement_requested = "calle del vocabulario"
                    break
                elif "calle del ser y estar" in text.lower():
                    self.movement_requested = "calle del ser y estar"
                    break
                elif "calle del instituto cervantes" in text.lower():
                    self.movement_requested = "calle del instituto cervantes"
                    break
                elif "avenida hablo español" in text.lower():
                    self.movement_requested = "avenida hablo español"
                    break
                elif "avenida porfe dele" in text.lower():
                    self.movement_requested = "avenida porfe dele"
                    break
                elif "calle del sustantivo" in text.lower():
                    self.movement_requested = "calle del sustantivo"
                    break
                elif "calle del me gusta" in text.lower():
                    self.movement_requested = "calle del me gusta"
                    break
                elif "calle de los errores" in text.lower():
                    self.movement_requested = "calle de los errores"
                    break
                elif "calle de por y para" in text.lower():
                    self.movement_requested = "calle de por y para"
                    breakpoint
                elif "calle del adjetivo" in text.lower():
                    self.movement_requested = "calle del adjetivo"
                    break
                elif "calle del siele" in text.lower():
                    self.movement_requested = "calle del siele"
                    break
                elif "calle de los deberes hechos" in text.lower():
                    self.movement_requested = "calle de los deberes hechos"
                    break
                elif "avenida del subjuntivo" in text.lower():
                    self.movement_requested = "avenida del subjuntivo"
                    break
                elif "avenida del indicativo" in text.lower():
                    self.movement_requested = "avenida del indicativo"
                    break
                elif "calle de los verbos" in text.lower():
                    self.movement_requested = "calle de los verbos"
                    break
                elif "calle de la gramatica" in text.lower():
                    self.movement_requested = "calle de la gramatica"
                    break
                elif "calle de las dudas" in text.lower():
                    self.movement_requested = "calle de las dudas"
                    break
                elif "calle de la n" in text.lower():
                    self.movement_requested = "calle de la n"
                    break       
                elif " " in text.lower():
                    print("no conozco ese lugar")

        else:
            print("no se hacer eso xd")
        

    def crearMatriz(self, x, y):
        matriz = []

        # Crear filas
        for i in range(21):
            fila = []
            # Crear columnas
            for j in range(26):
                fila.append('.')  # Agregar elementos vacíos a la fila
            matriz.append(fila)  # Agregar fila a la matriz
        matriz[x][y] = 'Q'
        return matriz

    def move_robot_to_school(self):
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
        return True
    
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

    
    def move_robot_to_university(self):
        # Calcular la dirección del movimiento hacia la escuela
        universidad = 'U'
        robotPos = (self.robot_block[0]-1,self.robot_block[1]-1)
        caminoPos = [(self.robot_block[0]-1,self.robot_block[1]-1)]
        camino = self.buscar_queso(self.matrizG, robotPos, caminoPos, universidad)
        print(str(camino))
        for coordenada in camino:
            next_block = (coordenada[0] + 1, coordenada[1] + 1)
            self.robot_block = next_block

            time.sleep(1)
            self.render()

    def move_robot_to_circo(self):
        while True:
            # Calcular la dirección del movimiento hacia el circo
            dx = self.circo_block[1] - self.robot_block[1]
            dy = self.circo_block[0] - self.robot_block[0]

            # Mover el robot bloque por bloque hacia el circo
            if dx != 0:
                # Mover horizontalmente
                step = dx // abs(dx)
                next_block = (self.robot_block[0], self.robot_block[1] + step)
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block
            elif dy != 0:
                # Mover verticalmente
                step = dy // abs(dy)
                next_block = (self.robot_block[0] + step, self.robot_block[1])
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block

            # Verificar si el robot ha llegado al circo
            if self.robot_block == self.circo_block:
                self.movement_requested = False
                break
            time.sleep(1)
            self.render()
    
    def move_robot_to_calle1(self):
        while True:
            # Calcular la dirección del movimiento hacia la calle 1
            dx = self.calle1_block[1] - self.robot_block[1]
            dy = self.calle1_block[0] - self.robot_block[0]

            # Mover el robot bloque por bloque hacia la calle 1
            if dx != 0:
                # Mover horizontalmente
                step = dx // abs(dx)
                next_block = (self.robot_block[0], self.robot_block[1] + step)
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block
            elif dy != 0:
                # Mover verticalmente
                step = dy // abs(dy)
                next_block = (self.robot_block[0] + step, self.robot_block[1])
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block

            # Verificar si el robot ha llegado a la calle 1
            if self.robot_block == self.calle1_block:
                self.movement_requested = False
                break
            time.sleep(1)
            self.render()
    def move_robot_to_calle2(self):
        while True:
            # Calcular la dirección del movimiento hacia la calle 2
            dx = self.calle2_block[1] - self.robot_block[1]
            dy = self.calle2_block[0] - self.robot_block[0]

            # Mover el robot bloque por bloque hacia la calle 2
            if dx != 0:
                # Mover horizontalmente
                step = dx // abs(dx)
                next_block = (self.robot_block[0], self.robot_block[1] + step)
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block
            elif dy != 0:
                # Mover verticalmente
                step = dy // abs(dy)
                next_block = (self.robot_block[0] + step, self.robot_block[1])
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block

            # Verificar si el robot ha llegado a la calle 2
            if self.robot_block == self.calle2_block:
                self.movement_requested = False
                break
            time.sleep(1)
            self.render()
    
    def move_robot_to_pizza(self):
        while True:
            # Calcular la dirección del movimiento hacia la pizzería
            dx = self.pizza_block[1] - self.robot_block[1]
            dy = self.pizza_block[0] - self.robot_block[0]

            # Mover el robot bloque por bloque hacia la pizzería
            if dx != 0:
                # Mover horizontalmente
                step = dx // abs(dx)
                next_block = (self.robot_block[0], self.robot_block[1] + step)
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block
            elif dy != 0:
                # Mover verticalmente
                step = dy // abs(dy)
                next_block = (self.robot_block[0] + step, self.robot_block[1])
                if next_block not in self.blocked_blocks:
                    self.robot_block = next_block

            # Verificar si el robot ha llegado a la pizzería
            if self.robot_block == self.pizza_block:
                self.movement_requested = False
                break
            time.sleep(1)
            self.render()