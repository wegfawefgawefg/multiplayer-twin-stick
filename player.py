import random
import pygame
from pygame import Vector2
from pygame import Vector3


class Player:
    WIDTH = 10
    SPEED = 10
    FIRE_DELAY = 30

    def __init__(self, pos):
        self.type = 'player'
        self.vel = Vector2(0, 0)
        self.pos = pos
        self.aim = Vector2(1, 0)
        self.color = Vector3(random.randint(100, 200))
        self.time_since_shot = 0
        self.shooting = False
        self.alive = True

    def kill(self):
        self.alive = False

    def aim_at(self, pos):
        self.aim = pos - self.pos
        self.aim.normalize_ip()

    def set_actions(self, actions):
        move_up_down = actions.get('my')
        move_left_right = actions.get('mx')
        shoot = actions.get('s')
        aim_x = actions.get('ax')
        aim_y = actions.get('ay')

        if move_up_down is not None:
            self.vel.y = move_up_down
        if move_left_right is not None:
            self.vel.x = move_left_right

        if self.vel != Vector2():
            self.vel = self.vel.normalize() * self.SPEED

        self.shooting = shoot

        if aim_x and aim_y:
            self.aim_at(Vector2(aim_x, aim_y))

    def update(self, dt):
        self.pos += self.vel * dt
        self.time_since_shot += dt

    def shoot(self):
        actually_shot = False
        if self.shooting:
            if self.time_since_shot > self.FIRE_DELAY:
                self.time_since_shot = 0
                actually_shot = True
            self.shooting = False
        return actually_shot

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.WIDTH)
        pygame.draw.line(surface, (0, 0, 255), self.pos,
                         self.pos + self.aim * 100)

    def get_state(self):
        return {
            'type': self.type,
            'pos': self.pos,
            'vel': self.vel,
            'aim': self.aim,
            'alive': self.alive,
            'color': self.color
        }

    def set_state(self, data):
        for key, value in data.items():
            if key == 'pos':
                self.pos = Vector2(value[0], value[1])
            elif key == 'vel':
                self.vel = Vector2(value[0], value[1])
            elif key == 'aim':
                self.aim = Vector2(value[0], value[1])
            elif key == 'alive':
                self.alive = value
            elif key == 'color':
                self.color = value
