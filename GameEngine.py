import math

from objects.Level import Level
from objects.Player import Player
from RaycastingEngine import RaycastingEngine
import tkinter as tk
from settings import *


class GameEngine:
    def __init__(self, width, height, level, player):
        self.width = width
        self.height = height
        self.level = level
        self.raycasting_engine = RaycastingEngine(width, height, self.level)
        self.player = player
        self.enemies = []
        self.npcs = []
        self.projectiles = []
        self.sprites = []
        self.actors = []

    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for npc in self.npcs:
            npc.update()
        for projectile in self.projectiles:
            projectile.update()

    def render(self, canvas):
        self.raycasting_engine.render(canvas, self.level, self.player)
        for enemy in self.enemies:
            enemy.render(canvas)
        for npc in self.npcs:
            npc.render(canvas)
        for projectile in self.projectiles:
            projectile.render(canvas)
        for sprite in self.sprites:
            sprite.render(canvas)
        for actor in self.actors:
            actor.render(canvas)

    def game_loop(self, root, canvas):
        self.update()
        canvas.delete("all")
        self.render(canvas)
        root.after(MS_PER_FRAME, self.game_loop(root, canvas))  # 60 fps


def main():
    root = tk.Tk()
    root.title("Raycaster")
    canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.pack()

    player = Player(PLAYER_X0, PLAYER_Y0, PLAYER_MOVEMENT_SPEED * MS_PER_FRAME / 1000,
                    math.radians(PLAYER_ROTATION_SPEED_DEGREES) * MS_PER_FRAME / 1000,
                    math.radians(FOV_DEGREES))
    level = Level(LEVEL_1_MAP)
    game_engine = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, player, level)

    root.after(MS_PER_FRAME, game_engine.game_loop(root, canvas))
    root.mainloop()
