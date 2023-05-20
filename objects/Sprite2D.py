from objects.GameObject import GameObject
from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk


# TODO directional sprite
class Sprite2D(GameObject):
    def __init__(self, x, y, radius, image_path):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = Image.open(image_path)
        self.photoImage = None

    def update(self, dt):
        pass

    def render(self, canvas, x, y, width, height, brightness):
        image_resized = self.image.resize((width, height))
        enhancer = ImageEnhance.Brightness(image_resized)
        image_resized = enhancer.enhance(brightness)
        self.photoImage = ImageTk.PhotoImage(image_resized)
        canvas.create_image(x, y, image=self.photoImage)
