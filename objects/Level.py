from utils import return_rotated_matrix


# TODO opening doors
class Level:
    def __init__(self, level_map, screen_height, screen_width):
        self.level_map = level_map
        self.level_map_rotated = return_rotated_matrix(self.level_map)
        self.map_tile_size = min(int(screen_height / len(self.level_map)), int(screen_width / len(self.level_map[0])))

    def load_from_file(self, file_path):
        pass

    def render(self, canvas):

        for y in range(0, len(self.level_map)):
            for x in range(0, len(self.level_map[y])):
                x0 = x * self.map_tile_size
                y0 = y * self.map_tile_size
                color = "black"
                if self.level_map[y][x] > 0:
                    color = "white"
                canvas.create_rectangle(x0, y0, x0 + self.map_tile_size, y0 + self.map_tile_size, fill=color, width=0)
        return canvas
