from commands.Command import Command

from objects.Actor import Actor


class MoveActorCommand(Command):

    def __init__(self, actor: Actor, dx: float, dy: float):
        self.actor = actor
        self.dx = dx
        self.dy = dy

    def execute(self):
        self.actor.move_to(self.actor.x + self.dx, self.actor.y + self.dy)
