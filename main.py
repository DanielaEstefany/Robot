import pygame
import sys
from game import Game

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width, height = 600, 400

# Crear la ventana
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mapa del robot")

# Crear una instancia del juego
game = Game(window, width, height)

# Ejecutar el juego
game.run()

# Salir de Pygame
pygame.quit()
sys.exit()