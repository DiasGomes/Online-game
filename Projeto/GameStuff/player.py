import pygame
import GameStuff.map as map
from GameStuff.spritesheet import SpriteSheet

class player:
    
    def __init__(self, _position, _size, _name):
        self.x, self.y = _position
        self.name = _name
        self.size = _size
        self.speed = 4
        self.shoot = False
        self.cooldown = 30
        self.cooldown_count = 0
        self.color = (0, 255, 0)
        self.sprites = SpriteSheet(pygame.image.load("GameStuff/sprites/player.png").convert_alpha(), 32, 32, 1)
        
    def move(self, comando):
        left_x = int(self.x // map.CELL_SIZE)
        right_x = int((self.x + self.size - 1) // map.CELL_SIZE)
        head_y = int(self.y // map.CELL_SIZE)
        bottom_y = int((self.y + self.size - 1) // map.CELL_SIZE)
        
        # movimento horizontal
        if comando == 0:
            future_x = int((self.x + self.size + self.speed - 1) // map.CELL_SIZE)
            if (map.MAP[future_x][head_y] != 0) and (map.MAP[future_x][bottom_y] != 0):
                self.x += self.speed
        elif comando == 1:
            future_x = int((self.x - self.speed) // map.CELL_SIZE)
            if (map.MAP[future_x][head_y] != 0) and (map.MAP[future_x][bottom_y] != 0):
                self.x -= self.speed
                
        # movimento vertical
        if comando == 2:
            future_y = int((self.y - self.speed) // map.CELL_SIZE)
            if (map.MAP[left_x][future_y] != 0) and (map.MAP[right_x][future_y] != 0):
                self.y -= self.speed
        elif comando == 3:
            future_y = int((self.y + self.size + self.speed - 1) // map.CELL_SIZE)
            if (map.MAP[left_x][future_y] != 0) and (map.MAP[right_x][future_y] != 0):
                self.y += self.speed
     
    def update(self):         
        # controle de cooldown
        if self.shoot:
            self.cooldown_count += 1
            if self.cooldown_count > self.cooldown:
                self.cooldown_count = 0
                self.shoot = False
    
    def render(self, g, cx, cy, font_size=10):
        pygame.draw.rect(g, self.color ,(self.x - cx, self.y - cy, self.size, self.size), 0)
        sprite = self.sprites.get_image(2)
        g.blit(sprite, (self.x - cx, self.y - cy))
        
        # desenha nome
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", font_size)                 
        render_font = font.render(self.name, 1, (0,0,0))
        g.blit(render_font, (self.x - cx, self.y + self.size + 2 - cy))
        pygame.display.flip()
        