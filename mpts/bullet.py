import pygame
from pygame import Vector2


class Bullet:
    SIZE = 10
    SPEED = 10

    def __init__(self, pos, direction):
        self.type = 'bullet'
        self.pos = pos
        self.direction = direction
        self.dead = False

    def kill(self):
        self.dead = True

    def update(self, dt):
        self.pos += self.direction * self.SPEED * dt

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.pos, self.SIZE)

    def get_state(self):
        return {
            'type': self.type,
            'pos': self.pos,
            'direction': self.direction
        }

    def set_state(self, data):
        for key, value in data.items():
            if key == 'pos':
                self.pos = Vector2(value[0], value[1])
            elif key == 'direction':
                self.direction = Vector2(value[0], value[1])
