''' client to connect and receive dicts from server '''
import socket
from pprint import pprint
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
        ''' send data to server '''
        self.sock.send(data)

    def receive(self):
        ''' receive data from server '''
        return self.sock.recv(1024)

    def close(self):
        ''' close connection '''
        self.sock.close()

if __name__ == '__main__':
    client = Client('localhost', 9999)
    while True:
        d = client.receive()
        di = json.loads(d.decode('utf-8'))
        pprint(di)
        client.send(b'ok')
