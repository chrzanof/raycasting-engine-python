class SpriteRender:
    """class encapsulating all params to render sprite"""
    # params - (sprite2D, isVisible, sprite_parameters)
    # sprite_parameters - (screen_x, SCREEN_HEIGHT/2,  width, height / 2, brightness)
    def __init__(self, params):
        self.params = params

    def render(self, canvas):
        if self.params[1]:
            self.params[0].render(canvas,
                                  self.params[2][0],
                                  self.params[2][1],
                                  self.params[2][2],
                                  self.params[2][3],
                                  self.params[2][4])
