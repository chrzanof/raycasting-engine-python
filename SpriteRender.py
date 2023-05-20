class SpriteRender:
    # params - (sprite2D, distance, isVisible, sprite_parameters)
    # sprite_parameters - (screen_x, SCREEN_HEIGHT/2,  width, height / 2, brightness)
    def __init__(self, params):
        self.params = params

    def render(self, canvas):
        if self.params[2]:
            self.params[0].render(canvas,
                                  self.params[3][0],
                                  self.params[3][1],
                                  self.params[3][2],
                                  self.params[3][3],
                                  self.params[3][4])
