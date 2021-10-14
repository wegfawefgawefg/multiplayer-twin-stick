import pygame
import pickle
import socket
from _game import Game


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.game = Game()
        self.last_actions = None

    def update(self):
        actions = self.game.player_actions
        if self.last_actions != actions:
            self.last_actions = actions
            self.socket.send(pickle.dumps(actions))
        else:
            self.socket.send(pickle.dumps(None))
        data = self.socket.recv(2048)
        if data:
            hydrated = pickle.loads(data)
            print(f'client received {hydrated}')
            self.game.set_state(hydrated)


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
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and
                 event.key == pygame.K_ESCAPE)):
                running = False

        client.game.handle_input(events)
        client.update()

        screen.fill((30, 20, 30))
        client.game.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
