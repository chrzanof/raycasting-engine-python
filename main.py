import time
from tkinter import *
from datetime import datetime
from math import *

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
screen_height = 768
screen_width = 768
screen_3d_offset_x = screen_width
screen_3d_offset_y = screen_height / 2
map_x = len(level_map[0])
map_y = len(level_map)
if screen_width / map_x != screen_height / map_y: raise Exception("Wrong window size")
map_s = screen_width / map_x
px = 400
py = 400
pa = 0.0
dpa = 0.1
fov = radians(60)
dpx = 0
dpy = 0
wall_color_horizontal = "#19fa21"
wall_color_vertical = "#0fb014"
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
    draw_map()
    draw_player()
    cast_rays()
    canvas.pack()


def draw_map():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, screen_width * 2, screen_height, fill="grey", width=0)
    canvas.create_rectangle(screen_width, 0, screen_width * 2, screen_height / 2, fill="#00FFFF", width=0)
    for x in range(0, map_y):
        for y in range(0, map_x):
            x0 = x * map_s
            y0 = y * map_s
            color = "black"
            if level_map[y][x] == 1:
                color = "white"
            canvas.create_rectangle(x0, y0, x0 + map_s, y0 + map_s, fill=color, width=0)


def draw_player():
    canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="yellow")
    canvas.create_line(px, py, px + 16 * cos(pa), py + 16 * sin(pa), fill="yellow", width=3)


def cast_rays():
    global px, py, pa
    ra = pa - fov / 2
    number_of_rays = 200
    dra = fov / number_of_rays
    for i in range(0, number_of_rays):
        if ra < 0:
            ra = ra + 2 * pi
        if ra > 2 * pi:
            ra = ra - 2 * pi
        x_step = 0
        y_step = 0
        player_tile_pos_y = int(py / map_s)
        player_tile_pos_x = int(px / map_s)

        if 0 < ra < pi:
            y_step = 1
        if pi < ra < 2 * pi:
            y_step = -1
        if 0 <= ra < 0.5 * pi or 1.5 * pi < ra <= 2 * pi:
            x_step = 1
        if 0.5 * pi < ra < 1.5 * pi:
            x_step = -1

        # horizontal check - green ray
        grdx, grdy, grh = 0, 0, 0
        if x_step != 0:
            reverse = 0
            if x_step == -1:
                reverse = 1

            if x_step == 1:
                grdx = (player_tile_pos_x + x_step) * map_s - px
            elif x_step == -1:
                grdx = player_tile_pos_x * map_s - px

            while True:
                grdy = grdx * tan(ra)
                grh = sqrt(grdx ** 2 + grdy ** 2)
                if 0 < int((py + grdy)) < screen_height:
                    if level_map[int((py + grdy - reverse) / map_s)][int((px + grdx - reverse) / map_s)] == 1:
                        break
                else:
                    break
                grdx += x_step * map_s
        else:
            grh = inf

        # vertical check -- yellow ray
        yrdx, yrdy, yrh = 0, 0, 0
        if y_step != 0:
            reverse = 0
            if y_step == -1:
                reverse = 1

            if y_step == 1:
                yrdy = (player_tile_pos_y + y_step) * map_s - py
            elif y_step == -1:
                yrdy = player_tile_pos_y * map_s - py

            while True:
                yrdx = yrdy * 1 / tan(ra)
                yrh = sqrt(yrdx ** 2 + yrdy ** 2)
                if 0 < int((px + yrdx)) < screen_width:
                    if level_map[int((py + yrdy - reverse) / map_s)][int((px + yrdx - reverse) / map_s)] == 1:
                        break
                else:
                    break
                yrdy += y_step * map_s
        else:
            yrh = inf



        if grh < yrh:
            wall_color = wall_color_horizontal
            canvas.create_line(px, py, px + grdx, py + grdy, fill=wall_color)
            wall_dist = grh
        else:
            wall_color = wall_color_vertical
            canvas.create_line(px, py, px + yrdx, py + yrdy, fill=wall_color)
            wall_dist = yrh

        ca = pa - ra
        if ca < 0:
            ca += 2 * pi
        if ca >= 2 * pi:
            ca -= 2 * pi
        wall_dist = wall_dist * cos(ca)  # fish eye effect correction
        line_height = screen_height * map_s / wall_dist

        screen_dx = wall_dist * tan(fov / 2) - wall_dist * tan(ca)
        a = screen_dx / (2 * wall_dist * tan(fov / 2))
        screen_position_x = screen_3d_offset_x + a * screen_width
        next_screen_position_x = screen_position_x
        if i < number_of_rays:
            screen_dx_next = wall_dist * tan(fov / 2) - wall_dist * tan(ca - dra)
            a_next = screen_dx_next / (2 * wall_dist * tan(fov / 2))
            next_screen_position_x = screen_3d_offset_x + a_next * screen_width

        if line_height > screen_height:
            line_height = screen_height
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
