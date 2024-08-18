from client import client
import pygame
import sys
import json

NOME_JOGO = "Nome do jogo"
FPS = 60
SIZE = 48

class player:
    
    def __init__(self, _position):
        self.x, self.y = _position
        self.size = SIZE
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
    
    def render(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.size, self.size), 0)

class Game:

    def __init__(self, _ip, _port):
        pygame.init()
        self.conection = client(_ip, _port)
        self.width, self.height = self.conection.screen_size
        self.screen = pygame.display.set_mode(self.conection.screen_size)
        pygame.display.set_caption(NOME_JOGO)
        self.player = player(self.conection.player_position)
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
            if self.player.x + self.player.size + self.player.speed < self.width:
                self.player.update(0)

        if keys[pygame.K_LEFT]:
            if self.player.x >= self.player.speed:
                self.player.update(1)

        if keys[pygame.K_UP]:
            if self.player.y >= self.player.speed:
                self.player.update(2)

        if keys[pygame.K_DOWN]:
            if self.player.y + self.player.size + self.player.speed < self.height:
                self.player.update(3)
                
        # atualiza informações para o servidor
        server_data = json.loads(self.update_server())
        
        # atualiza informações dos outros playes para o jogador
        for key, data in server_data.items():
            if (key != self.conection.id) and (data != ''):
                lst_pos = data.split(":")
                self.others[key] = {'x': int(lst_pos[0]), 'y': int(lst_pos[1])}

    # desenha o jogo
    def render(self):
        # desenha o fundo
        self.screen.fill((255,255,255))
        # desenha o player
        self.player.render(self.screen)
        # desenha todos os jogadores
        for _, _other in self.others.items():
            pygame.draw.rect(self.screen, (255, 0, 0) ,(_other['x'], _other['y'], SIZE, SIZE), 0)
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
    
