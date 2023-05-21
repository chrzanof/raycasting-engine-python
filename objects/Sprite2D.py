from PIL import Image, ImageTk, ImageEnhance

from objects.GameObject import GameObject


class Sprite2D(GameObject):

    def __init__(self, x, y, radius, render_radius, path):
        self.x = x
        self.y = y
        self.radius = radius
        self.render_radius = render_radius
        self.image = Image.open(path)
        self.photoImage = None

    def update(self, player_x, player_y, player_angle):
        pass

    def render(self, canvas, x, y, width, height, brightness):
        image_resized = self.image.resize((width, height))
        enhancer = ImageEnhance.Brightness(image_resized)
        image_resized = enhancer.enhance(brightness)
        self.photoImage = ImageTk.PhotoImage(image_resized)
        canvas.create_image(x, y, image=self.photoImage)


