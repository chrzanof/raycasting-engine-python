import time
from tkinter import *
from datetime import datetime
from math import *

screen_height = 512
screen_width = 512
screen_3d_offset_x = screen_width
screen_3d_offset_y = screen_height / 2
map_x = 8
map_y = 8
map_s = 64
px = 300
py = 300
pa = 1.5 * pi
dpa = 0.1
fov = radians(72)
dpx = 0
dpy = 0
wall_color_horizontal = "#19fa21"
wall_color_vertical = "#0fb014"
map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],

]
player_input = ""
player_movement_increment = 4
window = Tk()
window.title("Raycast Engine")
canvas = Canvas(window, height=screen_height, width=screen_width + 512)


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
    canvas.create_rectangle(0, 0, 1024, 512, fill="black")
    for x in range(0, map_y):
        for y in range(0, map_x):
            x0 = x * map_s
            y0 = y * map_s
            color = "black"
            if map[y][x] == 1:
                color = "white"
            canvas.create_rectangle(x0, y0, x0 + map_s, y0 + map_s, fill=color)


def draw_player():
    canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="yellow")
    canvas.create_line(px, py, px + 16 * cos(pa), py + 16 * sin(pa), fill="yellow", width=3)


def cast_rays():
    global px, py, pa
    ra = pa - fov / 2
    dra = fov / screen_width
    for i in range(0, screen_width):
        if ra < 0:
            ra = ra + 2 * pi
        if ra > 2*pi:
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
            hith = False

            if x_step == 1:
                grdx = (player_tile_pos_x + x_step) * map_s - px
            elif x_step == -1:
                grdx = player_tile_pos_x * map_s - px

            grdy = grdx * tan(ra)
            grh = sqrt(grdx ** 2 + grdy ** 2)
            if 0 < int((py + grdy)) < screen_height:
                if map[int((py + grdy - reverse) / map_s)][int((px + grdx - reverse) / map_s)] == 1:
                    hith = True
            else:
                hith = True

            while not hith:
                grdx += x_step * map_s
                grdy = grdx * tan(ra)
                grh = sqrt(grdx ** 2 + grdy ** 2)
                if 0 < int((py + grdy)) < screen_height:
                    if map[int((py + grdy - reverse) / map_s)][int((px + grdx - reverse) / map_s)] == 1:
                        hith = True
                else:
                    hith = True
        else:
            grh = inf

        # vertical check -- yellow ray
        yrdx, yrdy, yrh = 0, 0, 0
        if y_step != 0:
            reverse = 0
            if y_step == -1:
                reverse = 1
            hitv = False

            if y_step == 1:
                yrdy = (player_tile_pos_y + y_step) * map_s - py
            elif y_step == -1:
                yrdy = player_tile_pos_y * map_s - py

            yrdx = yrdy * 1 / tan(ra)
            yrh = sqrt(yrdx ** 2 + yrdy ** 2)
            if 0 < int((px + yrdx)) < screen_width:
                if map[int((py + yrdy - reverse) / map_s)][int((px + yrdx - reverse) / map_s)] == 1:
                    hitv = True
            else:
                hitv = True

            while not hitv:
                yrdy += y_step * map_s
                yrdx = yrdy * 1 / tan(ra)
                yrh = sqrt(yrdx ** 2 + yrdy ** 2)
                if 0 < int((px + yrdx)) < screen_width:
                    if map[int((py + yrdy - reverse) / map_s)][int((px + yrdx - reverse) / map_s)] == 1:
                        hitv = True
                else:
                    hitv = True
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
        wall_dist = wall_dist * cos(pa - ra)  # fish eye effect correction
        line_height = screen_height * map_s / wall_dist
        if line_height > screen_height:
            line_height = screen_height
        canvas.create_line(screen_3d_offset_x + i, screen_3d_offset_y - 0.5 * line_height, screen_3d_offset_x + i,
                           screen_3d_offset_y + 0.5 * line_height, fill=wall_color)

        ra = ra + dra


def loop():
    update()
    render_view()
    window.after(12, loop)


window.bind("<Key>", process_input)
window.after(12, loop)
window.mainloop()
