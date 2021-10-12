'''
we are going to make a basic game with a few players that shoot at eachother
characters aim with mouse, and move with arrow keys
can handle multiple players

multiplayer will be added afterwards
'''

import random
from pprint import pprint

import pygame
from pygame.math import Vector2

DIRECTIONS = set(["u", "d", "l", "r"])

class Player:
    WIDTH = 10
    SPEED = 10
    FIRE_DELAY = 30
    def __init__(self, pos, id):
        self.id = id
        self.vel = Vector2(0, 0)
        self.pos = pos
        self.aim = Vector2(1, 0)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.time_since_shot = 0
        self.shooting = False

    def aim_at(self, pos):
        self.aim = pos - self.pos
        self.aim.normalize_ip()

    def set_actions(self, actions):
        move_up_down = actions.get("mu")
        move_left_right = actions.get("mr")
        shoot = actions.get("s")
        aim_x = actions.get("ax")
        aim_y = actions.get("ay")

        if move_up_down:
            if move_up_down == "u":
                self.vel.y = -self.SPEED
            elif move_up_down == "d":
                self.vel.y = self.SPEED
        else:
            self.vel.y = 0
        if move_left_right:
            if move_left_right == "l":
                self.vel.x = -self.SPEED
            elif move_left_right == "r":
                self.vel.x = self.SPEED
        else:
            self.vel.x = 0

        self.shooting = shoot

        if aim_x and aim_y:
            self.aim_at(Vector2(aim_x, aim_y))

    def tic(self):
        self.pos += self.vel
        self.time_since_shot += 1

    def shoot(self, bullets):
        if self.shooting:
            if self.time_since_shot > self.FIRE_DELAY:
                pos = self.pos + self.aim * (self.WIDTH + Bullet.SIZE + 1.0) / 2
                bullets.append(Bullet(pos, self.aim))
                self.time_since_shot = 0
            self.shooting = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.WIDTH)
        pygame.draw.line(surface, (0, 0, 255), self.pos, self.pos + self.aim * 100)

    def serialize(self):
        return {
            "id": self.id,
            "px": self.pos.x,
            "py": self.pos.y,
            "ax": self.aim.x,
            "ay": self.aim.y,
            "cr": self.color[0],
            "cg": self.color[1],
            "cb": self.color[2],
        }
    
    def deserialize(self, data):
        self.id = int(data["id"])
        self.pos.x = int(data["px"])
        self.pos.y = int(data["py"])
        self.aim.x = int(data["ax"])
        self.aim.y = int(data["ay"])
        self.color = (int(data["cr"]), int(data["cg"]), int(data["cb"]))

class Bullet:
    SIZE = 10
    SPEED = 10
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def tic(self):
        self.pos += self.direction * self.SPEED

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.pos, self.SIZE)

    def serialize(self):
        return {
            "px": self.pos.x,
            "py": self.pos.y,
            "d": self.direction.x,
            "dy": self.direction.y,
        }

    def deserialize(self, data):
        self.pos.x = data["px"]
        self.pos.y = data["py"]
        self.direction.x = data["d"]
        self.direction.y = data["dy"]

class Game:
    def __init__(self):
        self.width = 500
        self.height = 500

        self.player_actions = {"mu":"", "mr":"", "s":False, "ax":-1, "ay":-1}

        self.id_to_player = {}
        self.players = []
        self.bullets = []

    def handle_input(self, player_id, data):
        self.id_to_player[player_id].act(data)

    def add_player(self, player_id):
        pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
        new_player = Player(pos, player_id)
        self.id_to_player[player_id] = new_player
        self.players.append(new_player)

    def remove_player(self, player_id):
        self.players.remove(self.id_to_player[player_id])
        del self.id_to_player[player_id]

    def draw(self, screen):
        for player in self.players:
            player.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)

    def tic(self):
        #pprint(self.player_actions)
        for bullet in self.bullets:
            bullet.tic()
        self.check_hits()
        self.clear_bullets()
        for player in self.players:
            player.tic()
            player.shoot(self.bullets)
        self.constrain_players()
    
    def clear_bullets(self):
        for bullet in self.bullets:
            if bullet.pos.x < 0 or bullet.pos.x > self.width or bullet.pos.y < 0 or bullet.pos.y > self.height:
                self.bullets.remove(bullet)

    def constrain_players(self):
        for player in self.players:
            player.pos.x = max(0, min(player.pos.x, self.width))
            player.pos.y = max(0, min(player.pos.y, self.height))

    def check_hits(self):
        for bullet in self.bullets:
            for player in self.players:
                if bullet.pos.distance_to(player.pos) < player.WIDTH:
                    self.bullets.remove(bullet)
                    del self.id_to_player[player.id]
                    self.players.remove(player)

    def serialize(self):
        return {
            'players': [player.serialize() for player in self.players],
            'bullets': [bullet.serialize() for bullet in self.bullets]
        }

    def deserialize(self, data):
        self.players = [Player.deserialize(player) for player in data['players']]
        self.bullets = [Bullet.deserialize(bullet) for bullet in data['bullets']]

    def handle_local_inputs(self, player_id, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # use wasd please
                if event.key == pygame.K_w:
                    self.player_actions["mu"] = "u"
                elif event.key == pygame.K_s:
                    self.player_actions["mu"] = "d"
                if event.key == pygame.K_a:
                    self.player_actions["mr"] = "l"
                elif event.key == pygame.K_d:
                    self.player_actions["mr"] = "r"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    if self.player_actions["mu"] == "u":
                        self.player_actions["mu"] = ""
                if event.key == pygame.K_s:
                    if self.player_actions["mu"] == "d":
                        self.player_actions["mu"] = ""
                if event.key == pygame.K_a:
                    if self.player_actions["mr"] == "l":
                        self.player_actions["mr"] = ""
                if event.key == pygame.K_d:
                    if self.player_actions["mr"] == "r":
                        self.player_actions["mr"] = ""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player_actions["s"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.player_actions["s"] = False

        mouse_pos = Vector2(*pygame.mouse.get_pos())
        self.player_actions["ax"] = mouse_pos.x
        self.player_actions["ay"] = mouse_pos.y

        self.id_to_player[player_id].set_actions(self.player_actions)

def main():
    pygame.init()
    pygame.display.set_caption('Shooter')
    screen = pygame.display.set_mode((500, 500))

    game = Game()
    local_player_id = 69
    game.add_player(local_player_id)
    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # handle press escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        game.handle_local_inputs(local_player_id, events)
        game.tic()

        if not local_player_id in game.id_to_player:
            game.add_player(local_player_id)

        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)