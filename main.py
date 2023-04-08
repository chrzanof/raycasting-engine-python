import time
from tkinter import *
from datetime import datetime
from math import *


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


level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]
level_map_rotated = return_rotated_matrix(level_map)
screen_height = 768
screen_width = 768
screen_3d_offset_x = screen_width
screen_3d_offset_y = screen_height / 2
map_x = len(level_map[0])
map_y = len(level_map)
if screen_width / map_x != screen_height / map_y: raise Exception("Wrong window size")
map_s = screen_width / map_x
px = 301
py = 650
pa = -0.1
dpa = 0.1
fov = radians(60)
dpx = 0
dpy = 0
wall_color_horizontal = rgb_to_hex((255, 0, 0))
wall_color_vertical = rgb_to_hex((200, 0, 0))
ceiling_color = rgb_to_hex((56, 56, 56))
floor_color = rgb_to_hex((117, 115, 116))
player_input = ""
player_movement_increment = 4
window = Tk()
window.title("Raycast Engine")
canvas = Canvas(window, height=screen_height, width=screen_width * 2)


def process_input(event):
    global player_input
    player_input = event.keysym


def update():
    global px
    global py
    global pa
    global player_input
    global dpx
    global dpy
    dpx = player_movement_increment * cos(pa)
    dpy = player_movement_increment * sin(pa)
    dpx90 = player_movement_increment * cos(pa + 0.5 * pi)
    dpy90 = player_movement_increment * sin(pa + 0.5 * pi)
    if player_input == "w":
        px += dpx
        py += dpy
    if player_input == "s":
        px -= dpx
        py -= dpy
    if player_input == "a":
        px -= dpx90
        py -= dpy90
    if player_input == "d":
        px += dpx90
        py += dpy90
    if player_input == "Left":
        pa -= dpa
        if pa < 0:
            pa += 2 * pi
    if player_input == "Right":
        pa += dpa
        if pa > 2 * pi:
            pa -= 2 * pi
    player_input = ""


def render_view():
    global canvas, px, py, pa
    canvas = draw_map(level_map, canvas)
    canvas = draw_player(canvas, px, py, pa)
    cast_rays()
    canvas.pack()


def draw_map(level, cv):
    cv.delete("all")
    cv.create_rectangle(0, 0, screen_width * 2, screen_height, fill=floor_color, width=0)
    cv.create_rectangle(screen_width, 0, screen_width * 2, screen_height / 2, fill=ceiling_color, width=0)
    for x in range(0, map_y):
        for y in range(0, map_x):
            x0 = x * map_s
            y0 = y * map_s
            color = "black"
            if level[y][x] == 1:
                color = "white"
            cv.create_rectangle(x0, y0, x0 + map_s, y0 + map_s, fill=color, width=0)
    return cv


def draw_player(cv, player_x, player_y, player_angle):
    cv.create_oval(player_x - 4, player_y - 4, player_x + 4, player_y + 4, fill="yellow")
    cv.create_line(player_x, player_y, player_x + 16 * cos(player_angle), player_y + 16 * sin(player_angle),
                   fill="yellow", width=3)
    return cv


def check_ray_length(ray_angle, player_x, player_y, level):
    player_tile_pos_x = int(player_x / map_s)
    reverse = 0
    step = 0
    ray_dx = 0
    if 0 <= ray_angle < 0.5 * pi or 1.5 * pi < ray_angle <= 2 * pi:
        step = 1
    if 0.5 * pi < ray_angle < 1.5 * pi:
        step = -1

    if step != 0:
        if step == 1:
            ray_dx = (player_tile_pos_x + step) * map_s - player_x
        elif step == -1:
            ray_dx = player_tile_pos_x * map_s - player_x
            reverse = 1

        while True:
            ray_dy = ray_dx * tan(ray_angle)
            ray_length = sqrt(ray_dx ** 2 + ray_dy ** 2)
            if 0 < int((player_y + ray_dy)) < screen_height:
                if level[int((player_y + ray_dy - reverse) / map_s)][int((player_x + ray_dx - reverse) / map_s)] == 1:
                    break
            else:
                break
            ray_dx += step * map_s
    else:
        ray_length = inf
    return ray_length


def return_rotated_player_position(player_x, player_y, angle_to_rotate):
    px_rotated = (player_x - screen_width / 2) * cos(radians(angle_to_rotate)) - (player_y - screen_height / 2) * sin(
        radians(angle_to_rotate))
    py_rotated = (player_x - screen_width / 2) * sin(radians(angle_to_rotate)) + (player_y - screen_height / 2) * cos(
        radians(angle_to_rotate))
    px_rotated = px_rotated + screen_width / 2
    py_rotated = py_rotated + screen_height / 2
    return px_rotated, py_rotated


def cast_rays():
    ra = pa - fov / 2
    number_of_rays = 200
    dra = fov / number_of_rays
    px_rotated, py_rotated = return_rotated_player_position(px, py, -90)
    for i in range(0, number_of_rays):
        if ra < 0:
            ra = ra + 2 * pi
        if ra > 2 * pi:
            ra = ra - 2 * pi

        # horizontal check - green ray
        horizontal_ray_len = check_ray_length(ra, px, py, level_map)

        # vertical check -- yellow ray
        ra_rotated = ra - radians(90)
        if ra_rotated < 0:
            ra_rotated = ra_rotated + 2 * pi
        if ra_rotated > 2 * pi:
            ra_rotated = ra_rotated - 2 * pi

        vertical_rey_len = check_ray_length(ra_rotated, px_rotated, py_rotated, level_map_rotated)

        if horizontal_ray_len < vertical_rey_len:
            wall_color = wall_color_horizontal
            wall_dist = horizontal_ray_len
        else:
            wall_color = wall_color_vertical
            wall_dist = vertical_rey_len

        # fish eye effect correction
        ca = pa - ra
        if ca < 0:
            ca += 2 * pi
        if ca >= 2 * pi:
            ca -= 2 * pi
        wall_dist = wall_dist * cos(ca)
        line_height = screen_height * map_s / wall_dist

        # calculating ray position on the screen
        screen_dx = wall_dist * tan(fov / 2) - wall_dist * tan(ca)
        a = screen_dx / (2 * wall_dist * tan(fov / 2))

        # calculating next ray position in order to fill the gap
        screen_position_x = screen_3d_offset_x + a * screen_width
        next_screen_position_x = screen_position_x
        if i < number_of_rays:
            screen_dx_next = wall_dist * tan(fov / 2) - wall_dist * tan(ca - dra)
            a_next = screen_dx_next / (2 * wall_dist * tan(fov / 2))
            next_screen_position_x = screen_3d_offset_x + a_next * screen_width

        if line_height > screen_height:
            line_height = screen_height

        color_scale_dist = 1 - min(wall_dist / (16 * map_s), 1)
        r, g, b = hex_to_rgb(wall_color)
        r = int(r * color_scale_dist)
        g = int(g * color_scale_dist)
        b = int(b * color_scale_dist)
        wall_color = rgb_to_hex((r, g, b))
        canvas.create_rectangle(screen_position_x, screen_3d_offset_y - 0.5 * line_height, next_screen_position_x,
                                screen_3d_offset_y + 0.5 * line_height, fill=wall_color, width=0)

        ra = ra + dra


def loop():
    update()
    render_view()

    window.after(12, loop)


window.bind("<Key>", process_input)
window.after(12, loop)
window.mainloop()
