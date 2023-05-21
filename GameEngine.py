import math

from InputHandler import InputHandler
from objects.DirectionalSprite import DirectionalSprite
from objects.Level import Level
from RaycastingEngine import RaycastingEngine
from objects.Texture import Texture
from objects.Sprite2D import Sprite2D


class GameEngine:
    def __init__(self, width, height, level_map, player, window):
        self.width = width
        self.height = height
        self.level = Level(level_map, height / 8, width / 8)
        self.player = player

        self.enemies = []
        self.npcs = []
        self.projectiles = []
        self.sprites = []
        self.actors = []
        self.inputHandler = InputHandler(window, player)

        self.textures = {
            1: Texture("textures/stone_wall32x32_1.ppm"),
            2: Texture("textures/stone_wall32x32_2.ppm"),
            3: Texture("textures/wooden_wall32x32.ppm"),
            4: Texture("textures/red_brick_wall32x32.ppm"),
            5: Texture("textures/metal_door32x32.ppm")
        }

        self.sprites.append(Sprite2D(10, 10, 0.5, 0.45, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(8, 8, 0.5, 0.45, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(10, 8, 0.5, 0.45, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(8, 10, 0.5, 0.45, "sprites/static/pillar.png"))

        self.sprites.append(Sprite2D(9, 9, 0.5, 0.45, "sprites/static/barrel.png"))
        self.sprites.append(Sprite2D(4.75, 1.5, 0.5, 0.45, "sprites/static/barrel.png"))

        self.sprites.append(Sprite2D(3, 3, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(6, 6, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(9, 9, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(12, 12, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(15, 15, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(3, 6, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(6, 9, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(9, 12, 0, 0.45, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(9, 15, 0, 0.45, "sprites/static/lamp.png"))

        self.sprites.append(DirectionalSprite(5, 3, 0.5, 0.45, math.radians(0), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(5, 4, 0.5, 0.45, math.radians(45), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(10.5, 5.5, 0.5, 0.45, math.radians(90), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(5, 10, 0.5, 0.45, math.radians(135), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(6, 5, 0.5, 0.45, math.radians(180), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(6, 11, 0.5, 0.45, math.radians(225), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(8.5, 8.5, 0.5, 0.45, math.radians(270), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(11.5, 11, 0.5, 0.45, math.radians(315), "sprites/directional/guard"))
        self.sprites.append(DirectionalSprite(2.5, 15, 0.5, 0.45, math.radians(270), "sprites/directional/guard"))

        self.raycasting_engine = RaycastingEngine(width, height, self.level, self.player, self.textures, self.sprites)

    def update(self):
        command_buffer = self.inputHandler.handle_input()
        for command in command_buffer:
            command.actor = self.player
            command.execute()

        collision = False

        for sprite in self.sprites:
            sprite.update(self.player.x, self.player.y, self.player.angle)
            if math.sqrt((self.player.x - sprite.x) ** 2 + (self.player.y - sprite.y) ** 2) < sprite.radius:
                collision = True

        self.level.update(self.player.x, self.player.y, self.player.angle)
        if self.level.level_map[int(self.player.y)][int(self.player.x)] != 0:
            collision = True

        if collision:
            for command in reversed(command_buffer):
                command.undo()

    def render(self, canvas):
        self.raycasting_engine.render(canvas)

        self.level.render(canvas)
        self.player.render(canvas, self.level.map_tile_size)

        return canvas
