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
        self.mapa = pygame.image.load("mapa.png")  # Reemplaza "nombre_del_archivo.png" con el nombre de tu imagen de mapa
        self.mapa = pygame.transform.scale(self.mapa, (self.width, self.height))

        self.blocked_blocks = (
            [(1, col) for col in range(1, 26)] +
            [(2, col) for col in range(1, 3)] + [(2, col) for col in range(5, 11)] + [(2, col) for col in range(13, 22)] + [(2, col) for col in range(24, 26)] +
            [(3, col) for col in range(1, 3)] + [(3, col) for col in range(5, 11)] + [(3, col) for col in range(13, 22)] + [(3, col) for col in range(24, 26)] +
            [(4, 1)]+ [(4, 3)] + [(4, 5)]+ [(4, 7)] + [(4, 9)]+ [(4, 10)] + [(4, 13)]+ [(4, 15)] + [(4, 16)]+ [(4, 3)] +
            [(10, col) for col in range(1, 3)] +
            [(11, col) for col in range(1, 3)] +
            [(12, 1)]+ [(12, 3)]+
            [(14, col) for col in range(1, 3)] + [(14, col) for col in range(5, 6)] + [(14, col) for col in range(8, 11)]
        )

        self.matrizG = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', '1', '#', ' ', '#', '2', '#', '3', '#', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', '#', ' ', '#', '#', ' ', ' ', '#', ' ', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
        ['#', 'E', '#', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', 'U', '#', ' ', '#', '#', '#', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        ['#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', '#', ' ', '#', '#', '#', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
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
        robot_x = (self.robot_block[1] - 1) * self.block_width + self.block_width // 2
        robot_y = (self.robot_block[0] - 1) * self.block_height + self.block_height // 2
        pygame.draw.circle(self.window, (255, 0, 0), (robot_x, robot_y), min(self.block_width, self.block_height) // 2)

        # Actualizar la ventana
        pygame.display.flip()

    def process_text(self, text):
        if "escuela" in text.lower():
            self.movement_requested = "escuela"
        elif "universidad" in text.lower():
            self.movement_requested = "universidad"
        elif "circo" in text.lower():
            self.movement_requested = "circo"
        elif "calle 1" in text.lower():
            self.movement_requested = "calle 1"
        elif "calle 2" in text.lower():
            self.movement_requested = "calle 2"
        elif "pizza" in text.lower():
            self.movement_requested = "pizza"
        

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
        school = 'E'
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