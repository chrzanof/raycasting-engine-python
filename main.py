from objects.DirectionalSprite import DirectionalSprite
from objects.Sprite2D import Sprite2D
from objects.Texture import Texture
from objects.Weapon import Weapon
from settings import *
import tkinter as tk
from objects.Player import Player
import math
from GameEngine import GameEngine
import time
"""
creating all objects and invoking game_loop() function
"""
window = tk.Tk()
window.title("Raycaster")
canvas = tk.Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()
level_1_map = [
    [1, 1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 5, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
textures = {
            1: Texture("textures/stone_wall32x32_1.ppm"),
            2: Texture("textures/stone_wall32x32_2.ppm"),
            3: Texture("textures/wooden_wall32x32.ppm"),
            4: Texture("textures/red_brick_wall32x32.ppm"),
            5: Texture("textures/metal_door32x32.ppm")
        }
sprites = [Sprite2D(10, 10, 0.5, 0.45, "sprites/static/pillar.png"),
           Sprite2D(8, 8, 0.5, 0.45, "sprites/static/pillar.png"),
           Sprite2D(10, 8, 0.5, 0.45, "sprites/static/pillar.png"),
           Sprite2D(8, 10, 0.5, 0.45, "sprites/static/pillar.png"),
           Sprite2D(9, 9, 0.5, 0.45, "sprites/static/barrel.png"),
           Sprite2D(4.75, 1.5, 0.5, 0.45, "sprites/static/barrel.png"),
           Sprite2D(3, 3, 0, 0.45, "sprites/static/lamp.png"), Sprite2D(6, 6, 0, 0.45, "sprites/static/lamp.png"),
           Sprite2D(9, 9, 0, 0.45, "sprites/static/lamp.png"), Sprite2D(12, 12, 0, 0.45, "sprites/static/lamp.png"),
           Sprite2D(15, 15, 0, 0.45, "sprites/static/lamp.png"), Sprite2D(3, 6, 0, 0.45, "sprites/static/lamp.png"),
           Sprite2D(6, 9, 0, 0.45, "sprites/static/lamp.png"), Sprite2D(9, 12, 0, 0.45, "sprites/static/lamp.png"),
           Sprite2D(9, 15, 0, 0.45, "sprites/static/lamp.png"),
           DirectionalSprite(5, 3, 0.5, 0.45, math.radians(0), "sprites/directional/guard"),
           DirectionalSprite(5, 4, 0.5, 0.45, math.radians(45), "sprites/directional/guard"),
           DirectionalSprite(10.5, 5.5, 0.5, 0.45, math.radians(90), "sprites/directional/guard"),
           DirectionalSprite(5, 10, 0.5, 0.45, math.radians(135), "sprites/directional/guard"),
           DirectionalSprite(6, 5, 0.5, 0.45, math.radians(180), "sprites/directional/guard"),
           DirectionalSprite(6, 11, 0.5, 0.45, math.radians(225), "sprites/directional/guard"),
           DirectionalSprite(8.5, 8.5, 0.5, 0.45, math.radians(270), "sprites/directional/guard"),
           DirectionalSprite(11.5, 11, 0.5, 0.45, math.radians(315), "sprites/directional/guard"),
           DirectionalSprite(2.5, 15, 0.5, 0.45, math.radians(270), "sprites/directional/guard")]

gun1 = Weapon(25, 1, False, "weapons/gun1.png")
gun2 = Weapon(15, 4, True, "weapons/gun2.png")
gun3 = Weapon(5, 20, True, "weapons/gun3.png")

player_x0 = 1.5
player_y0 = 1.5
player_angle0_degrees = 0
player_vertical_angle0_degrees = 0
player_max_vision_distance = 8
player_movement_speed = 10  # tiles per second
player_rotation_speed_degrees = 200  # degrees per second
player_radius = 0.25
player_fov_degrees = 90  # fov - field of view
player = Player(player_x0,
                player_y0,
                math.radians(player_angle0_degrees),
                player_movement_speed * MS_PER_FRAME / 1000,
                math.radians(player_rotation_speed_degrees) * MS_PER_FRAME / 1000,
                math.radians(player_fov_degrees),
                math.radians(player_vertical_angle0_degrees),
                player_max_vision_distance,
                player_radius,
                weapons=[gun1, gun2, gun3])

game_engine = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, level_1_map, player, window, textures, sprites)


def game_loop():
    """
    main loop in a game - invoking updates and rendering methods
    FPS calculation
    """
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
