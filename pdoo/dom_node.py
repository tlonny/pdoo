class DOMNode:
    def __init__(self, parent, tag_name, attrs):
        self.parent = parent
        self.children = list()
        self.tag_name = tag_name
        self.attributes = attrs

    def __enter__(self):
        self.document.parent_stack.append(self)

    def __exit__(self, exc_type, exc_value, traceback):
        self.document.parent_stack.pop()

    @property
    def document(self):
        return self.parent.document

    def render(self):
        fmtted_attrs = " ".join(f"{k}=\"{v}\"" for k, v in self.attributes.items())
        yield (0, f"<{self.tag_name} {fmtted_attrs}>" if len(fmtted_attrs) > 0 else f"<{self.tag_name}>")
        for child in self.children:
            for indent_count, line in child.render():
                yield (indent_count + 1, line)
        yield (0, f"</{self.tag_name}>")
