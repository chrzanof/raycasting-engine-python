from objects.GameObject import GameObject


class Sprite2D(GameObject):
    def __init__(self, x, y, texture_path):
        self.x = x
        self.y = y
        self.texture_path = texture_path

    def update(self, dt):
        pass

    def render(self, surface):
        pass
