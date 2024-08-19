import pygame

class SpriteSheet():
    def __init__(self, imagem, width, height, scale) -> None:
        self.imagem = imagem
        self.scale = scale
        self.img_width = width
        self.img_height = height
    
    def get_image(self, frame):
        image = pygame.Surface((self.img_width, self.img_height)).convert_alpha()
        image.blit(self.imagem, (0,0), ((frame * self.img_width),0,self.img_width, self.img_height))
        image = pygame.transform.scale(image, (self.img_width * self.scale, self.img_height * self.scale))
        return image