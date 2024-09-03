import pygame
import sys
import json
from client import client
from GameStuff.player import player
from GameStuff.bullet import bullet_
import GameStuff.map as map



NOME_JOGO = "Nome do jogo"
FPS = 60
FONT_SIZE = 5
SCREEN_WIDTH = map.CELL_SIZE * 16
SCREEN_HEIGHT = map.CELL_SIZE * 16
CENTER = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

class Game:

    def __init__(self, _username, _ip, _port):
        pygame.init()
        pygame.display.set_caption(NOME_JOGO)
        self.conection = client(_username, _ip, _port)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = player(self.conection.player_position, map.CELL_SIZE, _username)
        self.camera_x = self.player.x + (self.player.size / 2) - (SCREEN_WIDTH / 2)
        self.camera_y = self.player.y + (self.player.size / 2) - (SCREEN_HEIGHT / 2)
        self.mouse_x, self.mouse_y = (0,0)
        self.others = {}
        self.my_bullets = []

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
            self.player.move(0)
        if keys[pygame.K_LEFT]:
            self.player.move(1)
        if keys[pygame.K_UP]:
            self.player.move(2)
        if keys[pygame.K_DOWN]:
            self.player.move(3)
        self.player.update()
        
        # mouse info
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        atirou = pygame.mouse.get_pressed(num_buttons=3)
        
        # dispara 
        if atirou[0] and not self.player.shoot:
            self.player.shoot = True
            self.my_bullets.append(self.new_bullet())
            
        # atualiza informações para o servidor
        try:
            server_data = json.loads(self.update_server())
        except:
            self.erro_conection()
        # atualiza informações dos outros playes para o jogador
        for key, data in server_data.items():
            if (key != self.conection.id) and (data != ''):
                lst_pos = data['message'].split(";")
                self.others[key] = {'user':data['user'], 'x': int(lst_pos[0]), 'y': int(lst_pos[1])}
                
        # 
        for bullet in self.my_bullets:
            bullet.update()
            if bullet.destroy:
                self.my_bullets.remove(bullet)
        print(len(self.my_bullets))
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
            self.draw_text(_other['user'], _other['x'] - self.camera_x, _other['y'] - self.camera_y)
        
        # desenha bullets  
        for bullet in self.my_bullets:
            bullet.render(self.screen, self.camera_x, self.camera_y)
        
        pygame.draw.rect(self.screen, (120, 120, 255) , (CENTER[0], CENTER[1], 5, 5), 0)

        # atualiza display
        pygame.display.update()
    
    # escreve textos
    def draw_text(self, text, x, y, _font_type="comicsans"):
        pygame.font.init()
        font = pygame.font.SysFont(_font_type, FONT_SIZE)                   ##### coloca na posição 50,900 (tela FHD) 
        render_font = font.render(text, 1, (0,0,0))
        self.screen.blit(render_font, (x,y))
        
    def new_bullet(self):
        position = (self.player.x + map.CELL_SIZE/2, self.player.y + map.CELL_SIZE/2)
        dir_vetor = pygame.math.Vector2(self.mouse_x - CENTER[0], self.mouse_y - CENTER[1])
        direction = pygame.math.Vector2.normalize(dir_vetor)
        return bullet_(position, direction)
    
    # manda informações para o servidor
    def update_server(self):
        _data = str(self.player.x) + ";" + str(self.player.y)
        return self.conection.send_and_recv(_data)
    
    # fecha a conexao com o servidor
    def close(self):
        pygame.quit()
        self.conection.send_and_recv("quit")
        self.conection.close()
        sys.exit()
        
    def erro_conection(self):
        self.conection.send_and_recv("quit")
        self.conection.close()
        sys.exit()
    
