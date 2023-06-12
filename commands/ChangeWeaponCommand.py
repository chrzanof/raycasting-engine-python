from commands.Command import Command
from objects.Player import Player


class ChangeWeaponCommand(Command):
    def __init__(self, player: Player, index: int):
        self.player = player
        self.index = index
        self.index_before = 0

    def execute(self):
        """
        changes weapon to a given index
        :return:
        """
        self.index_before = self.index
        self.player.change_weapon(self.index)

    def undo(self):
        self.player.change_weapon(self.index_before)
