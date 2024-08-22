import pygame
import sys
import json
from client import client
from GameStuff.player import player
import GameStuff.map as map


NOME_JOGO = "Nome do jogo"
FPS = 60
SCREEN_WIDTH = map.CELL_SIZE * 16
SCREEN_HEIGHT = map.CELL_SIZE * 16

class Game:

    def __init__(self, _ip, _port):
        pygame.init()
        pygame.display.set_caption(NOME_JOGO)
        self.conection = client(_ip, _port)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = player(self.conection.player_position, map.CELL_SIZE)
        self.camera_x = self.player.x + (self.player.size / 2) - (SCREEN_WIDTH / 2)
        self.camera_y = self.player.y + (self.player.size / 2) - (SCREEN_HEIGHT / 2)
        self.mouse_x, self.mouse_y = (0,0)
        self.others = {}

    def run(self):     
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(FPS)
            
            # checa se fechou o jogo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    
            # dinamica do jogo    
            self.update()
            self.render()
    
    # logica do jogo
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.player.update(0)
        if keys[pygame.K_LEFT]:
            self.player.update(1)
        if keys[pygame.K_UP]:
            self.player.update(2)
        if keys[pygame.K_DOWN]:
            self.player.update(3)
        
        # mouse info
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        atirou = pygame.mouse.get_pressed(num_buttons=3)
        if atirou[0]:
            print("ATIROU")
        # atualiza informações para o servidor
        server_data = json.loads(self.update_server())
        
        # atualiza informações dos outros playes para o jogador
        for key, data in server_data.items():
            if (key != self.conection.id) and (data != ''):
                lst_pos = data.split(":")
                self.others[key] = {'x': int(lst_pos[0]), 'y': int(lst_pos[1])}
                
        # atualiza camera:
        self.camera_x = self.player.x + (self.player.size / 2) - (SCREEN_WIDTH / 2)
        self.camera_y = self.player.y + (self.player.size / 2) - (SCREEN_HEIGHT / 2)

    # desenha o jogo
    def render(self):
        # desenha o fundo
        self.screen.fill((255,255,255))
        map.draw_map(self.screen, self.camera_x, self.camera_y)
        # desenha o player
        self.player.render(self.screen, self.camera_x, self.camera_y)
        # desenha todos os jogadores
        for _, _other in self.others.items():
            pos = (_other['x'] - self.camera_x, _other['y'] - self.camera_y, map.CELL_SIZE, map.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0) , pos, 0)
            
        # draw mouse
        pygame.draw.rect(self.screen, (0, 0, 255) , (self.mouse_x, self.mouse_y, 5, 5), 0)
        
        # atualiza display
        pygame.display.update()
    
    # escreve textos
    def draw_text(self, text, size, x, y, _font_type="comicsans"):
        pygame.font.init()
        font = pygame.font.SysFont(_font_type, size)
        render = font.render(text, 1, (0,0,0))
        self.screen.draw(render, (x,y))
        
    # manda informações para o servidor
    def update_server(self):
        _data = str(self.player.x) + ":" + str(self.player.y)
        return self.conection.send_and_recv(_data)
    
    # fecha a conexao com o servidor
    def close(self):
        pygame.quit()
        self.conection.send_and_recv("quit")
        self.conection.close()
        sys.exit()
    
