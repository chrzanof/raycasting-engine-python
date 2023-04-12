import math

from objects.Actor import Actor


class Player(Actor):
    def __init__(self, x, y, angle, speed, rotation_speed, fov):
        super().__init__(x, y, angle, speed, rotation_speed, fov)

    def render(self, canvas, map_tile_size):
        canvas.create_oval(self.x * map_tile_size - 4, self.y * map_tile_size - 4, self.x * map_tile_size + 4, self.y * map_tile_size + 4, fill="yellow")
        canvas.create_line(self.x * map_tile_size, self.y * map_tile_size, self.x * map_tile_size + 16 * math.cos(self.angle), self.y * map_tile_size + 16 * math.sin(self.angle),
                           fill="yellow", width=3)
        return canvas