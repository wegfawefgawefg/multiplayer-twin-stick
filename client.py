import json
import socket
import threading
import time
import random

import pygame

from game import Game


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.game = Game()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.clients = []

    def accept_connections(self):
        while True:
            time.sleep(1/60)
            client, addr = self.sock.accept()
            self.clients.append(client)
            print('client connected')
            player_id = random.randint(0, 1000000)
            self.game.add_player(player_id)
            threading.Thread(target=self.handle_client, args=(client, addr, player_id)).start()

    def handle_client(self, client, addr, player_id):
        while True:
            try:
                time.sleep(1/60)
                client.send(json.dumps(self.game.serialize()).encode())
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

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.game = Game()

    #def send_input(self, input):
    #    self.sock.send(json.dumps(input))

    def sync_game(self):
        data = self.sock.recv(1024*4)
        if data:
            data = json.loads(data.decode())
            self.game.load_state(data)

def main():
    pygame.init()
    client = Client('localhost', 1234)

    pygame.display.set_caption('Shooter')
    screen = pygame.display.set_mode((500, 500))

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        client.sync_game()

        screen.fill((0, 0, 0))
        client.game.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()