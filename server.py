import json
import socket
import threading
import time
import random
from pprint import pprint
from game import Game

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
        self.game = Game()
        self.game.add_player(0)
        self.game.add_player(1)
        self.game.add_player(2)
        self.game.add_player(3)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.clients = []

    def accept_connections(self):
        print('waiting for connections')
        while True:
            time.sleep(1/60)
            client, addr = self.sock.accept()
            self.clients.append(client)
            print('client connected')
            player_id = random.randint(0, 1000000)
            self.game.add_player(player_id)
            threading.Thread(target=self.handle_client, args=(client, addr, player_id)).start()

    def handle_client(self, client, addr, player_id):
        print(f'new client {addr}, {player_id}')
        while True:
            try:
                time.sleep(1/60)
                print("sending")
                data = json.dumps(self.game.serialize()).encode()
                pprint(data)
                client.send(data)
                #data = client.recv(1024)
                #if data:
                #    print(data)
                #    data = json.loads(data)
                #    if data:
                #        self.game.handle_input(player_id, data)
                #else:
                #    self.clients.remove(client)
                #    self.game.remove_player(player_id)
                #    client.close()
                #    print('client disconnected')
                #    break
            except:
                self.clients.remove(client)
                self.game.remove_player(id)
                client.close()
                print('client disconnected')
                break

if __name__ == '__main__':
    server = Server('localhost', 1234)
    server.accept_connections()