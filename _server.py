import pickle
import socket
import threading
import time
import random
from uuid import uuid4

from _game import Game


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.game = Game()
        self.game.add_player(str(uuid4()))
        self.game.add_player(str(uuid4()))
        self.game.add_player(str(uuid4()))
        self.game.add_player(str(uuid4()))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.clients = {}

    def accept_connections(self):
        print('waiting for connections')
        while True:
            time.sleep(1/60)
            client, addr = self.sock.accept()
            self.clients[client] = []
            print('client connected')
            player_id = str(uuid4())
            self.game.add_player(player_id)
            thread = threading.Thread(
                target=self.handle_client,
                args=(client, addr, player_id)
            )
            thread.daemon = True
            thread.start()

    def handle_client(self, client, addr, player_id):
        print(f'new client {addr}, {player_id}')
        while True:
            time.sleep(1/60)
            data = client.recv(1024)
            if data:
                hydrated = pickle.loads(data)
                print(f'{addr} sent {hydrated}')
                if hydrated is not None:
                    self.game.handle_actions(hydrated, player_id)
                game_state = self.game.get_state()
                game_state = pickle.dumps(game_state)
                print(f'{addr} received {game_state}')
                client.send(game_state)

            #    self.clients.remove(client)
            #    self.game.remove_player(player_id)
            #    client.close()
            #    print('client disconnected')
            #    break


if __name__ == '__main__':
    server = Server('localhost', 1234)
    thread = threading.Thread(target=server.accept_connections)
    thread.daemon = True
    thread.start()
    while True:
        time.sleep(1/60)
        server.game.tic()
