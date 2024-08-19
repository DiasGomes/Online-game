from PIL import Image
import numpy as np
import pygame

from GameStuff.spritesheet import SpriteSheet

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

# transforma imagem em matriz de pixels
def getImagePixels():
    imagem = Image.open("GameStuff/sprites/mapa.png","r")
    return np.array(imagem), imagem.width, imagem.height

# converte matriz de pixels em matriz de inteiros
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

# desenha os tiles do jogos
def draw_map(g, cx, cy):
    for x, row in enumerate(MAP):
        for y, tile in enumerate(row):
            # parede
            if tile == 0:
                _imagem = spritesheet.get_image(1)
                g.blit(_imagem, ((x * CELL_SIZE) - cx, (y *CELL_SIZE) - cy))
            # chao
            else:
                _imagem = spritesheet.get_image(0)
                g.blit(_imagem, ((x * CELL_SIZE) - cx, (y *CELL_SIZE) - cy))

# recebe parametros da imagem do mapa do jogo
lst_pixels, pixel_width, pixel_height = getImagePixels()

# constantes
CELL_SIZE = 32
MAP_WIDTH = pixel_width * CELL_SIZE
MAP_HEIGHT = pixel_height * CELL_SIZE
MAP = getMatriz(lst_pixels)

spritesheet = SpriteSheet(pygame.image.load("GameStuff/sprites/tiles.png"), 16, 16, 2)