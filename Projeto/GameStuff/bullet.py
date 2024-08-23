import pygame
import GameStuff.map as map

class bullet_:
    
    def __init__(self, _position, _diretion):
        self.x, self.y = _position
        self.direction = _diretion
        self.size = 6
        self.speed = 5
        self.destroy = False
        self.color = (0, 0, 255)
        
    def update(self):
        self.x += (self.speed * self.direction[0])
        self.y += (self.speed * self.direction[1])
        
        x = int( (self.x + (self.size // 2)) // map.CELL_SIZE)
        y = int( (self.y + (self.size // 2)) // map.CELL_SIZE)
        if (map.MAP[x][y] == 0):
            self.destroy = True

        
    def render(self, g, cx, cy):
        pygame.draw.circle(g, self.color ,(self.x - cx, self.y - cy),  self.size, 0)
      