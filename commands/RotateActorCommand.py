from commands.Command import Command
from objects.Actor import Actor


class RotateActorCommand(Command):

    def __init__(self, actor: Actor, dest_angle: float):
        self.actor = actor
        self.dest_angle = dest_angle

    def execute(self, actor):
        actor.rotate_to(self.dest_angle)
