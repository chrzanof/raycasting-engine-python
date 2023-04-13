import math


def return_rotated_matrix(matrix):
    transpose_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    rotated_matrix = [row for row in transpose_matrix[::-1]]
    return rotated_matrix


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
