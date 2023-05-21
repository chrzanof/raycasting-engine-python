import math

from objects.Actor import Actor


class Player(Actor):
    def __init__(self, x, y, angle, speed, rotation_speed, fov, vertical_angle, vision_distance, radius, weapons):
        super().__init__(x, y, angle, speed, rotation_speed, fov, vertical_angle, vision_distance, radius)
        self.weapons = weapons
        self.selected_weapon = 0

    def render(self, canvas, map_tile_size):
        canvas.create_oval(self.x * map_tile_size - 2, self.y * map_tile_size - 2, self.x * map_tile_size + 2,
                           self.y * map_tile_size + 2, fill="yellow")
        canvas.create_line(self.x * map_tile_size, self.y * map_tile_size,
                           self.x * map_tile_size + 4 * math.cos(self.angle),
                           self.y * map_tile_size + 4 * math.sin(self.angle),
                           fill="green", width=3)
        if len(self.weapons) > 0:
            self.weapons[self.selected_weapon].render(canvas)
        return canvas

    def change_weapon(self, index):
        if 0 <= index < len(self.weapons):
            self.selected_weapon = index
