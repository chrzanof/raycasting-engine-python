import math

from InputHandler import InputHandler
from objects.DirectionalSprite import DirectionalSprite
from objects.Level import Level
from RaycastingEngine import RaycastingEngine
from objects.Texture import Texture
from objects.Sprite2D import Sprite2D


class GameEngine:
    def __init__(self, width, height, level_map, player, window, textures, sprites):
        self.width = width
        self.height = height
        self.level = Level(level_map, height / 8, width / 8)
        self.player = player
        self.sprites = sprites
        self.inputHandler = InputHandler(window, player)
        self.textures = textures
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
        self.player.render(canvas, self.level.map_tile_size)

        return canvas
