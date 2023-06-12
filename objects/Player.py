import math

from objects.Actor import Actor


class Player(Actor):
    def __init__(self, x, y, angle, speed, rotation_speed, fov, vertical_angle, vision_distance, radius, weapons):
        super().__init__(x, y, angle, speed, rotation_speed, fov, vertical_angle, vision_distance, radius)
        self.weapons = weapons
        self.selected_weapon = 0

    def render(self, canvas, map_tile_size):
        """
        renders selected weapon
        :param canvas:
        :param map_tile_size:
        :return: updated canvas
        """
        if len(self.weapons) > 0:
            self.weapons[self.selected_weapon].render(canvas)
        return canvas

    def change_weapon(self, index):
        """
        changes weapon
        :param index: weapon number
        :return:
        """
        if 0 <= index < len(self.weapons):
            self.selected_weapon = index
