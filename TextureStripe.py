class TextureStripe:

    def __init__(self, segments):
        self.segment_list = segments

    def render(self, canvas):
        for segment in self.segment_list:
            canvas.create_rectangle(segment[0], segment[1], segment[2], segment[3], fill=segment[4], width=segment[5])

        return canvas
