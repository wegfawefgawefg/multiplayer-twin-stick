import json
import socket
import threading
import time
import random

import pygame
from pprint import pprint

from game import Game

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.game = Game()

    def sync_game(self):
        self.sock.send(json.dumps(self.game.player_actions).encode())
        data = self.sock.recv(1024*8)
        if data:
            dec = data.decode()
            data = json.loads(dec)
            self.game.deserialize(data)

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

        client.game.handle_local_inputs(-1, events)
        client.sync_game()

        screen.fill((0, 0, 0))
        client.game.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()