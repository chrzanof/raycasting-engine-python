from commands.Command import Command
from objects.Actor import Actor


class RotateActorCommand(Command):

    def __init__(self, actor: Actor, d_angle: float):
        self.actor = actor
        self.d_angle = d_angle

    def execute(self):
        self.actor.rotate_to(self.actor.angle + self.d_angle)
