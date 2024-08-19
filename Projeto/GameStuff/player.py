import pygame
import GameStuff.map as map

class player:
    
    def __init__(self, _position, _size):
        self.x, self.y = _position
        self.size = _size
        self.speed = 2
        self.color = (0, 255, 0)
        
    def update(self, comando):
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
    
    def render(self, g, cx, cy):
        pygame.draw.rect(g, self.color ,(self.x - cx, self.y - cy, self.size, self.size), 0)
        