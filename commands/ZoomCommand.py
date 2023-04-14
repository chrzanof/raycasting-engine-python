import math

from commands.Command import Command

from objects.Actor import Actor
from settings import *


class ZoomCommand(Command):

    def __init__(self, actor: Actor, da: float):
        self.actor = actor
        self.da = da

    def execute(self):
        if math.radians(MIN_FOV_DEGREES) <= self.actor.fov + self.da <= math.radians(MAX_FOV_DEGREES):
            self.actor.fov = self.actor.fov + self.da
            ratio = SCREEN_HEIGHT / SCREEN_WIDTH
            angle_vertical = self.actor.fov * math.atan(ratio)
            self.actor.fov_vertical = angle_vertical
