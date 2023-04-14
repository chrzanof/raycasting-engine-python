from settings import *
import tkinter as tk
from objects.Player import Player
import math
from GameEngine import GameEngine

window = tk.Tk()
window.title("Raycaster")
canvas = tk.Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

player = Player(PLAYER_X0,
                PLAYER_Y0,
                math.radians(PLAYER_ANGLE0_DEGREES),
                PLAYER_MOVEMENT_SPEED * MS_PER_FRAME / 1000,
                math.radians(PLAYER_ROTATION_SPEED_DEGREES) * MS_PER_FRAME / 1000,
                math.radians(FOV_DEGREES),
                math.radians(PLAYER_VERTICAL_ANGLE0_DEGREES),
                PLAYER_MAX_VISION_DISTANCE)
game_engine = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_1_MAP, player, window)


def game_loop():
    global canvas
    game_engine.update()
    canvas.delete("all")
    canvas = game_engine.render(canvas)
    window.after(MS_PER_FRAME, game_loop)  # 60 fps


window.after(MS_PER_FRAME, game_loop)
window.mainloop()

