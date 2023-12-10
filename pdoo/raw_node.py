class RawNode:
    def __init__(self, raw):
        self.html = raw
    
    def render(self):
        yield (0, self.html)
