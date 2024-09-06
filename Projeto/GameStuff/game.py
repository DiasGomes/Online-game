import pygame
import ast
import sys
import json
from client import client
from GameStuff.player import player
from GameStuff.bullet import bullet_
import GameStuff.map as map

NOME_JOGO = "Nome do jogo"
FPS = 30
FONT_SIZE = 10
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
        self.other_bullets = []

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
    
    def update(self):
        # comandos de teclado
        self.teclado()
        # logica do player
        self.player.update()
        # acao de atirar e logica das bullets
        self.mouse()
        # atualiza informações para o servidor
        server_data = self.update_server()
        # logica dos outros players
        self.others_iteration(server_data)
        # atualiza camera:    
        self.camera()

    def render(self):
        # desenha o fundo/mapa
        self.screen.fill((105,205,255))
        map.draw_map(self.screen, self.camera_x, self.camera_y)
        # desenha o player
        self.player.render(self.screen, self.camera_x, self.camera_y)
        # desenha todos os jogadores
        self.draw_others()
        # desenha todos os projeteis
        self.draw_bullets()
        # atualiza display
        pygame.display.flip()
    
    def draw_text(self, text, x, y, _font_type="comicsans"):
        pygame.font.init()
        font = pygame.font.SysFont(_font_type, FONT_SIZE)           
        render_font = font.render(text, 1, (0,0,0))
        self.screen.blit(render_font, (x,y))
        
    def draw_others(self):
        for _, _other in self.others.items():
            xx = _other['x'] - self.camera_x
            yy = _other['y'] - self.camera_y
            pos = (xx, yy, map.CELL_SIZE, map.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0) , pos, 0)
            self.draw_text(_other['user'], xx + map.CELL_SIZE, yy + map.CELL_SIZE) 
        
        # esvazia buffer
        self.others = {}
            
    def draw_bullets(self):
        for bullet in self.my_bullets:
            bullet.render(self.screen, self.camera_x, self.camera_y)
        for bullet in self.other_bullets:
            bullet.render(self.screen, self.camera_x, self.camera_y)
        # esvazia buffer
        self.other_bullets = []
        
    def new_bullet(self):
        position = (self.player.x + map.CELL_SIZE/2, self.player.y + map.CELL_SIZE/2)
        dir_vetor = pygame.math.Vector2(self.mouse_x - CENTER[0], self.mouse_y - CENTER[1])
        direction = pygame.math.Vector2.normalize(dir_vetor)
        return bullet_(position, direction)
    
    def others_iteration(self, _server_data):
        # atualiza informações dos outros players para o jogador
        for key, data in _server_data.items():
            if (key != self.conection.id) and (data != ''):
                lst_pos = data['msg'].split(";")
                self.others[key] = {'user':data['user'], 'x': int(lst_pos[0]), 'y': int(lst_pos[1])}
                others_bullets = ast.literal_eval(lst_pos[2])
                for _bullet in others_bullets:
                    b_obj = bullet_(_bullet)
                    if (b_obj.x >= self.player.x) and (b_obj.x < self.player.x + self.player.size):
                        if (b_obj.y >= self.player.y) and (b_obj.y < self.player.y + self.player.size):
                            print("MORREU")
                            self.close()
                    self.other_bullets.append(b_obj)
    
    def update_server(self):
        # manda informações sobre o player
        bullets = []
        _response = {}
        for bullet in self.my_bullets:
            bullets.append((bullet.x, bullet.y))
        _data = str(self.player.x) + ";" + str(self.player.y) + ";" + str(bullets)
            
        try:
            _server_data = self.conection.send_and_recv(_data)
            _response = json.loads(_server_data)
        except Exception as e:
            print("ERRO: ", e)
            
        return _response
    
    def teclado(self):
        # controles
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.player.move(0)
        if keys[pygame.K_a]:
            self.player.move(1)
        if keys[pygame.K_w]:
            self.player.move(2)
        if keys[pygame.K_s]:
            self.player.move(3)
            
    def mouse(self):
        # mouse info
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        atirou = pygame.mouse.get_pressed(num_buttons=3)
        
        # dispara 
        if atirou[0] and not self.player.shoot:
            self.player.shoot = True
            self.my_bullets.append(self.new_bullet())
           
        # logica das balas
        for bullet in self.my_bullets:
            bullet.update()
            if bullet.destroy:
                self.my_bullets.remove(bullet)
                
    def camera(self):
        self.camera_x = self.player.x + (self.player.size / 2) - (SCREEN_WIDTH / 2)
        self.camera_y = self.player.y + (self.player.size / 2) - (SCREEN_HEIGHT / 2)
    
    def close(self):
        # fecha a conexao com o servidor
        pygame.quit()
        self.conection.send_and_recv("quit")
        self.conection.close()
        sys.exit()

