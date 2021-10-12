'''server to connect to clients, as many as possible
    send a example dictionary
'''

import socket
from pprint import pprint
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)

    def run(self):
        while True:
            client, addr = self.sock.accept()
            print('Connected by', addr)
            big_dict = {
                'name': 'john',
                'age': 20,
                'married': True,
                'children': ['jane', 'joe'],
                'pets': None,
                'cars': [
                    {'make': 'bmw', 'model': '550i'},
                    {'make': 'subaru', 'model': 'outback'},
                    {'make': 'audi', 'model': 'r8'},
                    {'make': 'subaru', 'model': 'outback'},
                    {'make': 'subaru', 'model': 'outback'},
                    {'make': 'subaru', 'model': 'outback'},
                ]
            }
            json_str = json.dumps(big_dict)
            d = json_str.encode()
            print(len(d))
            while True:
                client.send(d)
                client.recv(1024)

if __name__ == '__main__':
    s = Server('localhost', 9999)
    s.run()