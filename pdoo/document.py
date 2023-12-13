from textwrap import indent, dedent

from pdoo.dom_node import DOMNode
from pdoo.text_node import TextNode
from pdoo.raw_node import RawNode

class Document(DOMNode):
    def __init__(self, *, indent_size = 4):
        super().__init__(None, "html", dict())
        self.parent_stack = list()
        self.unique_id_gen = 0
        self.style_class_names = dict()
        self.indent_prefix = " " * indent_size

        with self:
            self.head = self.tag("head")
            self.body = self.tag("body")
        with self.head:
            self.auto_style = self.tag("style")


    def get_parent(self):
        return self.parent_stack[-1] if len(self.parent_stack) > 0 else self

    def tag(self, tag, attrs = dict(), text = None):
        parent = self.get_parent()
        tag_node = DOMNode(parent, tag, attrs)
        if text is not None:
            tag_node.children.append(TextNode(text))
        parent.children.append(tag_node)
        return tag_node

    def text(self, text):
        parent = self.get_parent()
        parent.children.append(TextNode(text))

    def raw(self, raw):
        parent = self.get_parent()
        parent.children.append(RawNode(raw))

    def attr(self, attr_name, attr_value):
        parent = self.get_parent()
        parent.attributes[attr_name] = attr_value

    def style(self, style_template):
        cache_key, style_lambda = style_template
        if cache_key not in self.style_class_names:
            # Include the function name in the class name to improve HTML debugging.
            # FQNs might have dots, which are not allowed in class names.
            class_name = f"cls-{cache_key[0]}-{cache_key[1]}-{self.unique_id_gen}".replace(".", "-")
            self.unique_id_gen += 1
            self.style_class_names[cache_key] = class_name
            with self.auto_style:
                rendered_template = style_lambda(class_name)
                self.raw(dedent(rendered_template).strip())
        return self.style_class_names[cache_key]

    @property
    def document(self):
        return self

    def __str__(self):
        return "\n".join([
            "<!DOCTYPE html>",
            * (indent(line, self.indent_prefix * indent_count) for indent_count, line in self.render())
        ])
