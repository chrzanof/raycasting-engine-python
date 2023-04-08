from objects.Actor import Actor


class Player(Actor):
    def __init__(self, x, y, angle, speed, rotation_speed, fov):
        super().__init__(x, y, angle, speed, rotation_speed, fov)

