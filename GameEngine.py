from InputHandler import InputHandler
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
        self.textures = []

        self.textures.append(Texture("textures/stone_wall32x32_1.ppm"))
        self.textures.append(Texture("textures/stone_wall32x32_2.ppm"))
        self.textures.append(Texture("textures/wooden_wall32x32.ppm"))
        self.textures.append(Texture("textures/red_brick_wall32x32.ppm"))
        self.textures.append(Texture("textures/metal_door32x32.ppm"))

        self.sprites.append(Sprite2D(6, 6, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(7, 6, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(6, 7, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(7, 7, "sprites/static/pillar.png"))
        self.sprites.append(Sprite2D(8.5, 8.5, "sprites/static/barrel.png"))
        self.sprites.append(Sprite2D(8.5, 8, "sprites/static/barrel.png"))
        self.sprites.append(Sprite2D(4, 1.5, "sprites/static/barrel.png"))
        self.sprites.append(Sprite2D(8.5, 8.5, "sprites/static/lamp.png"))
        self.sprites.append(Sprite2D(9, 9, "sprites/static/lamp.png"))

        self.raycasting_engine = RaycastingEngine(width, height, self.level, self.player, self.textures, self.sprites)

    def update(self):
        command_buffer = self.inputHandler.handle_input()
        for command in command_buffer:
            command.actor = self.player
            command.execute()

    def render(self, canvas):
        self.raycasting_engine.render(canvas)

        self.level.render(canvas)
        self.player.render(canvas, self.level.map_tile_size)

        return canvas
