'''server to connect to clients, as many as possible
    send a example dictionary
'''

import socket
from pprint import pprint
import json
import threading
import time

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)

    def accept_connections(self):
        while True:
            time.sleep(1/60)
            client, addr = self.sock.accept()
            print('Connected by', addr)
            threading.Thread(target=self.handle_client, args=(client, addr)).start()


    def handle_client(self, client, uuid):
            sample_data = {"haha": uuid}
            payload = json.dumps(sample_data).encode()
            while True:
                time.sleep(1/60)
                j = json.loads(client.recv(1024).decode())
                pprint(f"{uuid} {j}")
                client.send(payload)

if __name__ == '__main__':
    s = Server('localhost', 9999)
    s.accept_connections()