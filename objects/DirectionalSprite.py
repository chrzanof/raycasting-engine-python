import math

from objects.GameObject import GameObject
from objects.Sprite2D import Sprite2D
import os
from PIL import Image, ImageTk, ImageEnhance
from os import listdir


class DirectionalSprite(GameObject):

    def __init__(self, x, y, radius, render_radius, angle, folder_path):
        self.x = x
        self.y = y
        self.radius = radius
        self.render_radius = render_radius
        self.images = []
        self.angle = angle
        self.load_images(folder_path)
        self.image = self.images[0]
        self.photoImage = None

    def load_images(self, folder_path):
        for im in os.listdir(folder_path):
            if im.endswith(".png"):
                self.images.append(Image.open(folder_path + "/" + im))
        assert len(self.images) == 8

    def render(self, canvas, x, y, width, height, brightness):
        image_resized = self.image.resize((width, height))
        enhancer = ImageEnhance.Brightness(image_resized)
        image_resized = enhancer.enhance(brightness)
        self.photoImage = ImageTk.PhotoImage(image_resized)
        canvas.create_image(x, y, image=self.photoImage)

    def update(self, player_x, player_y, player_angle):
        beta = player_angle + math.radians(180) - self.angle
        if beta > 2 * math.pi:
            beta = beta - 2 * math.pi
        elif beta < 0:
            beta = beta + 2 * math.pi

        if 0 <= beta <= math.radians(22.5) or math.radians(360 - 22.5) <= beta < 0 :
            self.image = self.images[0]
        elif math.radians(22.5) < beta <= math.radians(90 - 22.5):
            self.image = self.images[-1]
        elif math.radians(90 - 22.5) < beta <= math.radians(135 - 22.5):
            self.image = self.images[-2]
        elif math.radians(135 - 22.5) < beta <= math.radians(180 - 22.5):
            self.image = self.images[-3]
        elif math.radians(180 - 22.5) < beta <= math.radians(225 - 22.5):
            self.image = self.images[-4]
        elif math.radians(225 - 22.5) < beta <= math.radians(270 - 22.5):
            self.image = self.images[-5]
        elif math.radians(270 - 22.5) < beta <= math.radians(315 - 22.5):
            self.image = self.images[-6]
        else:
            self.image = self.images[-7]

