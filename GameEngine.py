from InputHandler import InputHandler
from objects.Level import Level
from RaycastingEngine import RaycastingEngine


class GameEngine:
    def __init__(self, width, height, level_map, player, window):
        self.width = width
        self.height = height
        self.level = Level(level_map, height / 8, width / 8)
        self.player = player
        self.raycasting_engine = RaycastingEngine(width, height, self.level, self.player)
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
        self.raycasting_engine.render(canvas)
        self.level.render(canvas)
        self.player.render(canvas, self.level.map_tile_size)
        return canvas
