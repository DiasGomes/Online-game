import socket
import json

class client():

    def __init__(self, _username, _ip_host, _port=5555):
        # UDP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.username = _username
        self.addr = (_ip_host, _port)
        self.id, self.player_position = self.connect()

    def connect(self):  
        response = self.send_and_recv("try connect")
    
        # trata a informação
        msg = response.split(";")
        _id = msg[0]
        _player_position = (int(msg[1]), int(msg[2]))
        print(f"Client {_id} connected.\n Position: {_player_position}")
        
        return _id, _player_position 
    
    def send_and_recv(self, data: str)-> str:
        self.send_udp(data)
        return self.recv_udp()
    
    def send_udp(self, data: str):
        msg = {
            "user": self.username,
            "msg": data,
        }
        message = str.encode(json.dumps(msg))
        self.client.sendto(message, self.addr)

    def recv_udp(self) -> str:
        try:           
            reply, origin = self.client.recvfrom(2048)
            return reply.decode()
        except socket.error as e:
            return str(e)
        
    def close(self):
        self.client.close()
        print(f"Connection close!")