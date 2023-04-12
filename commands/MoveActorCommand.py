from commands.Command import Command

from objects.Actor import Actor


class MoveActorCommand(Command):

    def __init__(self, actor: Actor, dest_x: int, dest_y: int):
        self.actor = actor
        self.dest_x = dest_x
        self.dest_y = dest_y

    def execute(self, actor):
        actor.move_to(self.dest_x, self.dest_y)
