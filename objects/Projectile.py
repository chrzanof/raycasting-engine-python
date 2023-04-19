from objects.GameObject import GameObject


class Projectile(GameObject):
    def update(self, dt):
        pass

    def render(self, canvas):
        pass

    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed