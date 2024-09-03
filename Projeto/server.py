import socket
from _thread import *
import sys
import json

# parametros
server = ""
port = 5555
HEADER_LENGHT = 2048
data = {}
lst_position = [
    (64,64), (100, 64), (200, 64), (400, 64), (64, 400), 
    (100, 400), (200, 400), (400, 400), (64, 200), (400, 200)
]

# parametros por linha de comando [ip, porta]
if len(sys.argv) > 1:
    server = sys.argv[1]
    if len(sys.argv) > 2:
        port = sys.argv[2]

print("Waiting for a connection")

# fica escutando
while True:   
    # cria socket UDP
    server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        server_udp_socket.bind((server, port))
    except socket.error as e:
        print(str(e))
    
    # fica escutando
    b_response, addr = server_udp_socket.recvfrom(2048)
    str_response = b_response.decode('utf-8')
    msg_recv = json.loads(str_response)
    id = str(addr[0]) + "-" + str(addr[1])
    
    # se não existe adiciona nos dados
    if id not in data:
        x, y = lst_position[len(data)]
        msg =  str(x) + ";" + str(y)
        server_udp_socket.sendto(str.encode(id + ";" + msg), addr)
        msg_recv['message'] = msg
    
    try:
        print(f"client {id}: {msg_recv}")
        data[id] = msg_recv
        if msg_recv['message'] == "quit":
            # remove cliente da conexão
            print(f"Server: Goodbye {id}")
            server_udp_socket.sendto(str.encode(json.dumps({'Server': f'Goodbye {id}'})), addr)
            del data[id]
        # reenvia a msg para todos
        else:
            data_to_send = str.encode(json.dumps(data))
            server_udp_socket.sendto(data_to_send, addr)
    except Exception as e:
        print("ERRO: ", e)
        break
    