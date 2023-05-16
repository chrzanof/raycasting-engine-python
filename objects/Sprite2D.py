from objects.GameObject import GameObject
from PIL import Image, ImageTk
import tkinter as tk


class Sprite2D(GameObject):
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = Image.open(image_path)
        self.photoImage = None

    def update(self, dt):
        pass

    def render(self, canvas, x, y, width, height):
        image_resized = self.image.resize((width, height))
        self.photoImage = ImageTk.PhotoImage(image_resized)
        canvas.create_image(x, y, image=self.photoImage)
