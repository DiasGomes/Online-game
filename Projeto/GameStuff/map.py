from PIL import Image
import numpy as np
import pygame

# cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
YELLOW = (255,255, 0)
PINK = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 125, 0)

def getImagePixels():
    imagem = Image.open("GameStuff/sprites/mapa.png","r")
    return np.array(imagem), imagem.width, imagem.height

def getMatriz(lst_pixels):
    mapa = []

    for row in lst_pixels:
        linha = []
        for obj in row:
            cor = (obj[0], obj[1], obj[2])
            if cor == BLACK:
                linha.append(0)
            elif cor == GREEN:
                linha.append(2)
            else:
                linha.append(1)
        mapa.append(linha)
    return mapa

def draw_map(g, cx, cy):
    for x, row in enumerate(MAP):
        for y, tile in enumerate(row):
            cor = CYAN
            if tile == 0:
                cor = BLACK
            pos = ((x * CELL_SIZE) - cx, (y *CELL_SIZE) - cy, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(g, cor , pos, 0)
            #self.screen.blit(self.img_mapa, (-self.camera_x, -self.camera_y))


lst_pixels, pixel_width, pixel_height = getImagePixels()

# constantes
CELL_SIZE = 32
MAP_WIDTH = pixel_width * CELL_SIZE
MAP_HEIGHT = pixel_height * CELL_SIZE
MAP = getMatriz(lst_pixels)