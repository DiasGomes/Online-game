import pygame
import GameStuff.map as map
from GameStuff.spritesheet import SpriteSheet

class player:
    
    def __init__(self, _position, _size, _name, _sprites):
        self.x, self.y = _position
        self.name = _name
        self.size = _size
        self.speed = 4
        self.shoot = False
        self.cooldown = 30
        self.cooldown_count = 0
        self.color = (10, 55, 155)
        self.sprites = _sprites
        self.sprite_index = 2
        self.animation_count = 0
        self.sprite_animation = 0
        
    def move(self, comando):
        left_x = int(self.x // map.CELL_SIZE)
        right_x = int((self.x + self.size - 1) // map.CELL_SIZE)
        head_y = int(self.y // map.CELL_SIZE)
        bottom_y = int((self.y + self.size - 1) // map.CELL_SIZE)
        
        # parado
        if comando == -1:
            self.sprite_index = 2
        else:
            # movimento horizontal
            if comando == 0:
                self.sprite_index = 3 + self.sprite_animation
                future_x = int((self.x + self.size + self.speed - 1) // map.CELL_SIZE)
                if (map.MAP[future_x][head_y] != 0) and (map.MAP[future_x][bottom_y] != 0):
                    self.x += self.speed
            elif comando == 1:
                self.sprite_index = 0 + self.sprite_animation
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
                
        # controle animacao
        self.animation_count += 1
        if self.animation_count >= 20:
            self.animation_count = 0
            self.sprite_animation = 1 - self.sprite_animation
    
    def render(self, g, cx, cy, font_size=10):
        pygame.draw.rect(g, self.color ,(self.x - cx, self.y - cy, self.size, self.size), 0)
        sprite = self.sprites.get_image(self.sprite_index)
        g.blit(sprite, (self.x - cx, self.y - cy))
        
        # desenha nome
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", font_size)                 
        render_font = font.render(self.name, 1, (0,0,0))
        g.blit(render_font, (self.x - cx, self.y + self.size + 2 - cy))
        

        