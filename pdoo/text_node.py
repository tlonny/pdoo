from html import escape

class TextNode:
    def __init__(self, text):
        self.text = text

    def render(self):
        yield (0, escape(self.text))
