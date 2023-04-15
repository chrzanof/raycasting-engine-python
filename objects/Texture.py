from utils import *


class Texture:
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.rgb_array = []
        self.load()

    def load(self):
        file = open(self.texture_path, "r")
        file.readline()
        file.readline()
        data_row = file.readline()
        data_row = data_row.strip("\n")
        texture_dim_x, texture_dim_y = data_row.split(" ")
        texture_dim_x = int(texture_dim_x)
        texture_dim_y = int(texture_dim_y)
        file.readline()
        pixels = []
        pixel = []
        while data_row:
            data_row = file.readline()
            if data_row:
                pixel.append(int(data_row))
                if len(pixel) == 3:
                    pixels.append(pixel)
                    pixel = []
        file.close()
        assert len(pixels) == texture_dim_x * texture_dim_y
        texture_row = []
        dim_x_counter = 0
        for p in pixels:
            texture_row.append(p)
            dim_x_counter += 1
            if dim_x_counter >= texture_dim_x:
                self.rgb_array.append(texture_row)
                texture_row = []
                dim_x_counter = 0

    def render(self, canvas):
        for j in range(len(self.rgb_array)):
            for i in range(len(self.rgb_array[j])):
                r = self.rgb_array[i][j][0]
                g = self.rgb_array[i][j][1]
                b = self.rgb_array[i][j][2]
                canvas.create_rectangle(i, j, i, j, fill=rgb_to_hex((r, g, b)), width=0)

        return canvas
