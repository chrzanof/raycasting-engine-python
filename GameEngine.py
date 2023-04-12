import math

from InputHandler import InputHandler
from objects.Level import Level
from objects.Player import Player
from RaycastingEngine import RaycastingEngine
import tkinter as tk
from settings import *


class GameEngine:
    def __init__(self, width, height, level_map, player, window):
        self.width = width
        self.height = height
        self.level = Level(level_map, height, width)
        self.raycasting_engine = RaycastingEngine(width, height, self.level)
        self.player = player
        self.enemies = []
        self.npcs = []
        self.projectiles = []
        self.sprites = []
        self.actors = []
        self.inputHandler = InputHandler(window, player)

    def update(self):
        command_buffer = self.inputHandler.handle_input()
        for command in command_buffer:
            command.actor = self.player
            command.execute()

    def render(self, canvas):
        self.level.render(canvas)
        self.player.render(canvas, self.level.map_tile_size)
        return canvas


window = tk.Tk()
window.title("Raycaster")
canvas = tk.Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

player = Player(PLAYER_X0,
                PLAYER_Y0,
                math.radians(PLAYER_ANGLE0_DEGREES),
                PLAYER_MOVEMENT_SPEED * MS_PER_FRAME / 1000,
                math.radians(PLAYER_ROTATION_SPEED_DEGREES) * MS_PER_FRAME / 1000,
                math.radians(FOV_DEGREES))
game_engine = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_1_MAP, player, window)


def game_loop():
    global canvas
    game_engine.update()
    canvas.delete("all")
    canvas = game_engine.render(canvas)
    window.after(MS_PER_FRAME, game_loop)  # 60 fps
    canvas.pack()


window.after(MS_PER_FRAME, game_loop)
window.mainloop()
