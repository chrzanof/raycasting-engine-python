from objects.Texture import Texture
from objects.Weapon import Weapon
from settings import *
import tkinter as tk
from objects.Player import Player
import math
from GameEngine import GameEngine
import time
window = tk.Tk()
window.title("Raycaster")
canvas = tk.Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()
gun1 = Weapon(25, 1, False, "weapons/gun1.png")
gun2 = Weapon(15, 4, True, "weapons/gun2.png")
gun3 = Weapon(5, 20, True, "weapons/gun3.png")
player = Player(PLAYER_X0,
                PLAYER_Y0,
                math.radians(PLAYER_ANGLE0_DEGREES),
                PLAYER_MOVEMENT_SPEED * MS_PER_FRAME / 1000,
                math.radians(PLAYER_ROTATION_SPEED_DEGREES) * MS_PER_FRAME / 1000,
                math.radians(FOV_DEGREES),
                math.radians(PLAYER_VERTICAL_ANGLE0_DEGREES),
                PLAYER_MAX_VISION_DISTANCE,
                PLAYER_RADIUS,
                weapons=[gun1, gun2, gun3])

game_engine = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_1_MAP, player, window)


def game_loop():
    global canvas, previous_time, current_time
    previous_time = current_time
    current_time = time.time()
    elapsed_time = current_time - previous_time
    fps = int(1 / elapsed_time)
    window.title("Raycaster       FPS - " + str(fps))
    game_engine.update()
    canvas.delete("all")
    canvas = game_engine.render(canvas)
    window.after(MS_PER_FRAME, game_loop)  # 60 fps


previous_time = 0
current_time = 0
window.after(MS_PER_FRAME, game_loop)
window.mainloop()
