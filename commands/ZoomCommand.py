import math

from commands.Command import Command

from objects.Actor import Actor
from settings import *


class ZoomCommand(Command):

    def __init__(self, actor: Actor, da: float):
        self.actor = actor
        self.da = da
        self.fov_before = 0
        self.fov_vertical_before = 0

    def execute(self):
        if math.radians(MIN_FOV_DEGREES) <= self.actor.fov + self.da <= math.radians(MAX_FOV_DEGREES):
            self.fov_before = self.actor.fov
            self.fov_vertical_before = self.actor.fov_vertical
            self.actor.fov = self.actor.fov + self.da
            ratio = SCREEN_HEIGHT / SCREEN_WIDTH
            angle_vertical = self.actor.fov * math.atan(ratio)
            self.actor.fov_vertical = angle_vertical

    def undo(self):
        self.actor.fov = self.fov_before
        self.actor.fov_vertical = self.fov_vertical_before

