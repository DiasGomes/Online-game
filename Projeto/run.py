import sys
import GameStuff.game as game

if __name__ == "__main__":
    
    # parametros
    ip = ""
    port = 5555
    username = "player"

    # parametros por linha de comando [ip, porta]
    if len(sys.argv) > 1:
        ip = sys.argv[1]
        if len(sys.argv) > 2:
            username = sys.argv[2]
            if len(sys.argv) > 3:
                port = sys.argv[3]

    # começa o jogo
    g = game.Game(username, ip, port)
    g.run()
    
