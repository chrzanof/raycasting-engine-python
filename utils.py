import math
from settings import *


def return_rotated_matrix(matrix):
    t = [[0 for col in range(len(matrix[row]))] for row in range(len(matrix))]
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            t[len(matrix) - 1 - j][i] = matrix[i][j]
    return t


def rgb_to_hex(rgb):
    return "#" + '%02x%02x%02x' % rgb


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def return_rotated_actor_position(actor_x, actor_y, angle_to_rotate, max_x, max_y):
    x_rotated = (actor_x - max_y / 2) * math.cos(math.radians(angle_to_rotate)) - (actor_y - max_x / 2) * math.sin(math.radians(angle_to_rotate))
    y_rotated = (actor_x - max_y / 2) * math.sin(math.radians(angle_to_rotate)) + (actor_y - max_x / 2) * math.cos(math.radians(angle_to_rotate))
    x_rotated = x_rotated + max_y / 2
    y_rotated = y_rotated + max_x / 2
    return x_rotated, y_rotated
