import math

from settings import DOOR_INDEX

from utils import return_rotated_matrix


class Level:
    def __init__(self, level_map, screen_height, screen_width):
        self.level_map = level_map
        self.level_map_rotated = return_rotated_matrix(self.level_map)
        self.map_tile_size = min(int(screen_height / len(self.level_map)), int(screen_width / len(self.level_map[0])))

    def render(self, canvas):
        """
        renders level in 2D view
        :param canvas:
        :return: updated canvas
        """
        for y in range(0, len(self.level_map)):
            for x in range(0, len(self.level_map[y])):
                x0 = x * self.map_tile_size
                y0 = y * self.map_tile_size
                color = "black"
                if self.level_map[y][x] > 0:
                    color = "white"
                canvas.create_rectangle(x0, y0, x0 + self.map_tile_size, y0 + self.map_tile_size, fill=color, width=0)
        return canvas

    def update(self, player_x, player_y, player_angle):
        """
        updates all elements of the level that player can interact with. Right now only opens doors
        :param player_x:
        :param player_y:
        :param player_angle:
        :return:
        """
        # opening doors
        vector_end_x = player_x + 0.75 * math.cos(player_angle)
        vector_end_y = player_y + 0.75 * math.sin(player_angle)
        if 0 <= vector_end_x < len(self.level_map) and 0 <= vector_end_y <= len(self.level_map_rotated):
            if self.level_map[int(vector_end_y)][int(vector_end_x)] == DOOR_INDEX:
                self.level_map[int(vector_end_y)][int(vector_end_x)] = 0
                self.level_map_rotated = return_rotated_matrix(self.level_map)
