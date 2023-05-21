from PIL import Image, ImageTk

from settings import *


class Weapon:
    def __init__(self, damage, speed, auto, image_path):
        self.damage = damage
        self.speed = speed
        self.auto = auto
        self.image = Image.open(image_path)
        self.photoImage = None

    def update(self):
        pass

    def render(self, canvas):
        image_resized = self.image.resize((SCREEN_HEIGHT, SCREEN_HEIGHT))
        self.photoImage = ImageTk.PhotoImage(image_resized)
        canvas.create_image(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, image=self.photoImage)
        return canvas
