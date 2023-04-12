class InputHandler:

    def __init__(self, window):
        self.window = window
        self.key_buffer = []
        self.window.bind("<KeyPress>", self.keydown)
        self.window.bind("<KeyRelease>", self.keyup)

    def keyup(self, e):
        if e.keycode in self.key_buffer:
            self.key_buffer.pop(self.key_buffer.index(e.keycode))
            print(self.key_buffer)

    def keydown(self, e):
        if e.keycode not in self.key_buffer:
            self.key_buffer.append(e.keycode)
            print(self.key_buffer)
