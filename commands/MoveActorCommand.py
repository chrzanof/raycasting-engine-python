from commands.Command import Command

from objects.Actor import Actor


class MoveActorCommand(Command):

    def __init__(self, actor: Actor, dx: float, dy: float):
        self.actor = actor
        self.dx = dx
        self.dy = dy
        self.x_before = 0
        self.y_before = 0

    def execute(self):
        self.x_before = self.actor.x
        self.y_before = self.actor.y
        self.actor.move_to(self.actor.x + self.dx, self.actor.y + self.dy)

    def undo(self):
        self.actor.move_to(self.x_before, self.y_before)
