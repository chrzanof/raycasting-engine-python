from objects.GameObject import GameObject


class Actor(GameObject):
    def __init__(self, x, y, angle, speed, rotation_speed, fov):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.fov = fov

    def update(self, dt):
        pass

    def render(self, surface):
        pass
