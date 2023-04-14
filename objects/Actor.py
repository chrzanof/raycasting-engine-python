import math

from objects.GameObject import GameObject
from settings import *


class Actor(GameObject):
    def update(self, dt):
        pass

    def render(self, surface):
        pass

    def __init__(self, x, y, angle, speed, rotation_speed, fov):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.fov = fov
        self.fov_vertical = self.fov * math.atan(SCREEN_HEIGHT / SCREEN_WIDTH)

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def rotate_to(self, angle):
        self.angle = angle


