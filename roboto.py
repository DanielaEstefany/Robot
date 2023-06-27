import pygame
import sys
import speech_recognition as sr

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width, height = 800, 600

# Crear la ventana
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mapa del robot")

# Cargar la imagen del mapa
mapa = pygame.image.load("mapa.png")  # Reemplaza "nombre_del_archivo.png" con el nombre de tu imagen de mapa

# Redimensionar la imagen al tamaño de la ventana
mapa = pygame.transform.scale(mapa, (width, height))

# Tamaño de los bloques
block_width = width // 26
block_height = height // 21

# Posición inicial del robot en el mapa
robot_block = (1, 1)  # Bloque inicial del robot (fila, columna)

# Variable para controlar el bucle principal del juego
running = True

# Variable para controlar el movimiento del robot
movement_requested = False

# Crear un reconocedor de voz
recognizer = sr.Recognizer()

# Función para procesar el texto reconocido
def process_text(text):
    global robot_block
    if text.lower() == "avanzar a la derecha":
        robot_block = (robot_block[0], min(26, robot_block[1] + 1))
        movement_requested = True

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar la tecla presionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                robot_block = (max(1, robot_block[0] - 1), robot_block[1])
                movement_requested = True
            elif event.key == pygame.K_DOWN:
                robot_block = (min(21, robot_block[0] + 1), robot_block[1])
                movement_requested = True
            elif event.key == pygame.K_LEFT:
                robot_block = (robot_block[0], max(1, robot_block[1] - 1))
                movement_requested = True
            elif event.key == pygame.K_RIGHT:
                robot_block = (robot_block[0], min(26, robot_block[1] + 1))
                movement_requested = True

    # Utilizar el micrófono como fuente de audio
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=8)  # Escuchar el audio del micrófono sin límite de tiempo

        try:
            # Reconocer el texto utilizando el reconocedor de voz
            text = recognizer.recognize_google(audio, language="es")  # Puedes cambiar el idioma aquí

            # Imprimir el texto reconocido en la consola
            print("Texto reconocido:")
            print(text)

            # Procesar el texto reconocido
            process_text(text)

        except sr.UnknownValueError:
            print("No se pudo reconocer el audio.")

        except sr.RequestError as e:
            print("Error al solicitar los resultados del reconocimiento de voz; {0}".format(e))

    # Limpiar la ventana con un color de fondo
    window.fill((255, 255, 255))

    # Dibujar el mapa en la ventana
    window.blit(mapa, (0, 0))

    # Dibujar líneas verticales para los bloques
    for col in range(1, 26):
        x = col * block_width
        pygame.draw.line(window, (0, 0, 0), (x, 0), (x, height))

    # Dibujar líneas horizontales para los bloques
    for row in range(1, 21):
        y = row * block_height
        pygame.draw.line(window, (0, 0, 0), (0, y), (width, y))

    # Dibujar el robot en la posición actual
    robot_x = (robot_block[1] - 1) * block_width + block_width // 2
    robot_y = (robot_block[0] - 1) * block_height + block_height // 2
    pygame.draw.circle(window, (255, 0, 0), (robot_x, robot_y), min(block_width, block_height) // 2)

    # Actualizar la ventana
    pygame.display.flip()

    # Esperar hasta que se levante la tecla presionada antes de permitir otro movimiento del robot
    if movement_requested:
        movement_requested = False
        pygame.time.wait(200)  # Pausa de 200 milisegundos entre cada movimiento del robot

# Salir de Pygame
pygame.quit()
sys.exit()