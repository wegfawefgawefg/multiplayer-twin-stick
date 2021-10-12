''' client to connect and receive dicts from server '''
import socket
from pprint import pprint
import time
import json

class Client:
    ''' client to connect and receive dicts from server '''
    def __init__(self, host, port):
        ''' init client '''
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, data):
        try:
            self.sock.send(json.dumps(data).encode())
            return self.sock.recv(2048).decode()
        except socket.error as e:
            print(e)

if __name__ == '__main__':
    client = Client('localhost', 9999)
    while True:
        time.sleep(1/60)
        d = client.send({"wow":1})
        pprint(json.loads(d))
