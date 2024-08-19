import socket

class client():

    def __init__(self, _ip_host, _port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = _ip_host 
        self.port = _port
        self.addr = (self.host, self.port)
        self.id, self.player_position = self.connect()

    # conecta com o servidor
    def connect(self):
        # recebe parametros iniciais do servidor
        self.client.connect(self.addr)
        response = self.client.recv(2048).decode()
        
        # trata a informação
        msg = response.split(";")
        _id = msg[0]
        _player_position = (int(msg[1]), int(msg[2]))
        print(f"Client {_id} connected.\n Position: {_player_position}")
        
        return _id, _player_position 

    # envia e recebe dados do servidor
    def send_and_recv(self, data: str) -> str:
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
        
    # fecha conexão com o servidor
    def close(self):
        self.client.close()
        print(f"Connection close!")