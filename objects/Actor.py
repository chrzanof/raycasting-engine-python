import math

from objects.GameObject import GameObject
from settings import *


# TODO actor collision with walls and other things
class Actor(GameObject):
    def update(self):
        pass

    def render(self, canvas):
        pass

    def __init__(self, x, y, angle, speed, rotation_speed, fov, vertical_angle, vision_distance):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.fov = fov
        self.fov_vertical = self.fov * math.atan(SCREEN_HEIGHT / SCREEN_WIDTH)
        self.vertical_angle = vertical_angle
        self.vision_distance = vision_distance

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def rotate_to(self, angle):
        self.angle = angle
        if self.angle >= 2 * math.pi:
            self.angle = self.angle - 2 * math.pi
        elif self.angle < 0:
            self.angle = self.angle + 2 * math.pi
