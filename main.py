import time
from tkinter import *
from datetime import datetime
from math import *

map_x = 8
map_y = 8
map_s = 64
px = 300
py = 300
pa = 0.0
dpa = 0.1
dpx = 0
dpy = 0
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
window.title("test")
canvas = Canvas(window, height=512, width=1024)


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
            pa - 2 * pi
    player_input = ""


def render_view():
    draw_map()
    draw_player()
    canvas.pack()


def draw_map():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 1024, 512, fill="grey")
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


def loop():
    update()
    render_view()
    window.after(12, loop)


window.bind("<Key>", process_input)
window.after(12, loop)
window.mainloop()
