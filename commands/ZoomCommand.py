from commands.Command import Command

from objects.Actor import Actor


class ZoomCommand(Command):

    def __init__(self, actor: Actor, da: float):
        self.actor = actor
        self.da = da

    def execute(self):
        self.actor.fov = self.actor.fov + self.da
