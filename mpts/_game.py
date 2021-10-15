import random
import pygame
from uuid import uuid4
from pygame import Vector2
from _player import Player
from _bullet import Bullet


class Game:
    def __init__(self):
        self.width = 500
        self.height = 500

        self.player_actions = {
            'my': 0,
            'mx': 0,
            's': False,
            'ax': -1,
            'ay': -1
        }
        self.mouse_pos = Vector2(0, 0)

        self.entities = {}
        self.players = set()
        self.bullets = set()

        self.keys = {
            'up': set([pygame.K_w, pygame.K_UP]),
            'down': set([pygame.K_s, pygame.K_DOWN]),
            'left': set([pygame.K_a, pygame.K_LEFT]),
            'right': set([pygame.K_d, pygame.K_RIGHT])
        }

    def handle_actions(self, actions, uuid):
        self.entities[uuid].set_actions(actions)

    def handle_input(self, events, uuid=None):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.keys['up']:
                    self.player_actions['my'] = -1
                elif event.key in self.keys['down']:
                    self.player_actions['my'] = 1
                elif event.key in self.keys['left']:
                    self.player_actions['mx'] = -1
                elif event.key in self.keys['right']:
                    self.player_actions['mx'] = 1
            elif event.type == pygame.KEYUP:
                if event.key in self.keys['up'] and self.player_actions['my'] == -1:
                    self.player_actions['my'] = 0
                elif event.key in self.keys['down'] and self.player_actions['my'] == 1:
                    self.player_actions['my'] = 0
                elif event.key in self.keys['left'] and self.player_actions['mx'] == -1:
                    self.player_actions['mx'] = 0
                elif event.key in self.keys['right'] and self.player_actions['mx'] == 1:
                    self.player_actions['mx'] = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player_actions['s'] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.player_actions['s'] = False

        mouse_pos = Vector2(pygame.mouse.get_pos())
        if mouse_pos != self.mouse_pos:
            self.mouse_pos = mouse_pos
            self.player_actions['ax'] = mouse_pos.x
            self.player_actions['ay'] = mouse_pos.y

        if uuid:
            self.handle_actions(self.player_actions, uuid)

    def add_player(self, uuid):
        pos = Vector2(random.randint(0, self.width),
                      random.randint(0, self.height))
        new_player = Player(pos, uuid)
        self.entities[uuid] = new_player
        self.players.add(uuid)

    def remove_player(self, uuid):
        self.players.remove(uuid)
        del self.entities[uuid]

    def tic(self):
        for bullet_id in self.bullets:
            self.entities[bullet_id].tic()
        self.check_hits()
        self.clear_dead()
        for player_id in self.players:
            self.entities[player_id].tic()
        self.constrain_players()

    def player_shoot(self, player):
        if player.shoot():
            pos = player.pos + player.aim * \
                (player.WIDTH + Bullet.SIZE + 1.0) / 2
            bullet = Bullet(pos, player.aim)
            uuid = str(uuid4())
            self.entities[uuid] = bullet
            self.bullets.add(uuid)

    def check_hits(self):
        for bullet_id in self.bullets:
            bullet = self.entities[bullet_id]
            for player_id in self.players:
                player = self.entities[player_id]
                if bullet.pos.distance_to(player.pos) < player.WIDTH:
                    self.bullets.remove(bullet)
                    self.remove_player(player.uuid)
                    self.add_player(player.uuid)

    def clear_dead(self):
        for uuid, entity in self.entities.items():
            if not entity.alive:
                if entity.__class__ == Player:
                    self.players.remove(uuid)
                else:
                    self.bullets.remove(uuid)
                del self.entities[uuid]

    def constrain_players(self):
        for player_id in self.players:
            player = self.entities[player_id]
            player.pos.x = max(0, min(player.pos.x, self.width))
            player.pos.y = max(0, min(player.pos.y, self.height))

    def get_state(self):
        return {uuid: entity.get_state() for uuid, entity in self.entities.items()}

    def set_state(self, state):
        for uuid, entity in state.items():
            if uuid not in self.entities:
                self.create_entity(uuid, entity)
            self.entities[uuid].set_state(state[uuid])

    def create_entity(self, entity_id, data):
        entity_type = data['type']
        if entity_type == 'player':
            self.add_player(entity_id)
        elif entity_type == 'bullet':
            pos = Vector2(data['pos'])
            aim = Vector2(data['aim'])
            bullet = Bullet(pos, aim)
            self.entities[entity_id] = bullet
            self.bullets.add(entity_id)
        else:
            raise ValueError('Unknown entity type: {}'.format(entity_id))

    def draw(self, screen):
        for player_id in self.players:
            self.entities[player_id].draw(screen)
        for bullet_id in self.bullets:
            self.entities[bullet_id].draw(screen)
