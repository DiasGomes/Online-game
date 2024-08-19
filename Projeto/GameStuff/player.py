import pygame

class player:
    
    def __init__(self, _position, _size):
        self.x, self.y = _position
        self.size = _size
        self.speed = 2
        self.color = (0, 255, 0)
        
    def update(self, comando):
        # horizontal
        if comando == 0:
            self.x += self.speed
        elif comando == 1:
            self.x -= self.speed
        # vertical
        if comando == 2:
            self.y -= self.speed
        if comando == 3:
            self.y += self.speed
    
    def render(self, g, cx, cy):
        pygame.draw.rect(g, self.color ,(self.x - cx, self.y - cy, self.size, self.size), 0)