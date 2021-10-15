import pygame
from pygame import Vector2

from mpts.player import Player
from mpts.bullet import Bullet

pygame.init()


class Game:
    def __init__(self, server_mode=False, client=None):
        self.scale = 1
        self.screen_size = Vector2(500, 500)
        self.clock = pygame.time.Clock()
        self.server_mode = server_mode
        self.client = client

        if not server_mode:
            self.scr = pygame.Surface(self.screen_size, pygame.SRCALPHA)
            self.disp = pygame.display.set_mode((self.screen_size*self.scale))

        self.entities = {}

        self.keys = {
            'up': set([pygame.K_w, pygame.K_UP]),
            'down': set([pygame.K_s, pygame.K_DOWN]),
            'left': set([pygame.K_a, pygame.K_LEFT]),
            'right': set([pygame.K_d, pygame.K_RIGHT])
        }

    def set_client(self, client):
        self.client = client

    def run(self):
        assert self.client, 'Client not set'
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()
            self.client.sendMessage(event)

        self.update()
        self.draw()

    def new_player(self, uuid):
        pos = Vector2(self.screen_size)/2
        player = Player(pos)
        self.entities[uuid] = player

    def remove_player(self, uuid):
        self.entities[uuid].kill()

    def update(self):
        dt = self.clock.get_time()*.001
        self.clock.tick()

        # update logic here
        for entity in self.entities.values():
            entity.update(dt)

        if self.server_mode and self.client:
            self.update_connected_clients()

        self.clean_dead_entities()

    def clean_dead_entities(self):
        # cleanup dead entities
        to_remove = [uuid for uuid, entity in self.entities.items()
                     if entity.dead]
        for uuid in to_remove:
            del self.entities[uuid]

    def update_connected_clients(self):
        self.client.updateConnectedClients(self.get_state())

    def get_state(self):
        return {uuid: entity.get_state() for uuid, entity in self.entities.items()}

    def draw(self):
        self.scr.fill((30, 20, 30))

        # draw logic here
        for entity in self.entities.values():
            if hasattr(entity, 'draw'):
                entity.draw(self.scr)

        pygame.transform.scale(self.scr, self.disp.get_size(), self.disp)
        pygame.display.flip()

    def process_action(self, uuid, action):
        event = pygame.event.Event(action['type'], action['data'])
        entity = self.entities[uuid]
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys['up']:
                entity.vel.y = -100
            elif event.key in self.keys['down']:
                entity.vel.y = 100
            elif event.key in self.keys['left']:
                entity.vel.x = -100
            elif event.key in self.keys['right']:
                entity.vel.x = 100
        elif event.type == pygame.KEYUP:
            if event.key in self.keys['up'] and entity.vel.y == -100:
                entity.vel.y = 0
            elif event.key in self.keys['down'] and entity.vel.y == 100:
                entity.vel.y = 0
            elif event.key in self.keys['left'] and entity.vel.x == -100:
                entity.vel.x = 0
            elif event.key in self.keys['right'] and entity.vel.x == 100:
                entity.vel.x = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                entity.shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                entity.shooting = False
        elif event.type == pygame.MOUSEMOTION:
            entity.aim_at(event.pos)

    def process_state(self, state):
        for uuid, entity_state in state.items():
            if uuid not in self.entities:
                if entity_state['type'] == 'player':
                    self.entities[uuid] = Player(
                        entity_state['pos'])
                elif entity_state['type'] == 'bullet':
                    self.entities[uuid] = Bullet(entity_state['pos'])
            self.entities[uuid].set_state(entity_state)
