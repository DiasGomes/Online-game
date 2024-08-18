import sys
import game

if __name__ == "__main__":
    
    # parametros
    ip = ""
    port = 5555

    # parametros por linha de comando [ip, porta]
    if len(sys.argv) > 1:
        ip = sys.argv[1]
        if len(sys.argv) > 2:
            port = sys.argv[2]
    
    # começa o jogo
    g = game.Game(ip, port)
    g.run()
    
