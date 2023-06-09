from utils import *


class Texture:
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.rgb_array = []
        self.rgb_array_reversed = []
        self.load()

    def load(self):
        """loading texture from file to the array of pixels in rgb format"""
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
        self.create_reversed()

    def create_reversed(self):
        """reverses the texture in x dimension """
        for row in self.rgb_array:
            row_reversed = []
            for i in range(len(row) - 1, -1, -1):
                row_reversed.append(row[i])
            self.rgb_array_reversed.append(row_reversed)

    def render(self, canvas):
        """
        rendering texture in 2D view (only for testing)
        :param canvas:
        :return: updated canvas
        """
        for j in range(len(self.rgb_array)):
            for i in range(len(self.rgb_array[j])):
                r = self.rgb_array[j][i][0]
                g = self.rgb_array[j][i][1]
                b = self.rgb_array[j][i][2]
                canvas.create_rectangle(i, j, i, j, fill=rgb_to_hex((r, g, b)), width=0)

        return canvas

