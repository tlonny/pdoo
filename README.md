# PDOO

PDOO, short for "**P**ython **DO**M **O**rchestrator," is a lightweight, dependency-free library designed for effortlessly crafting styled HTML documents solely with Python. Drawing inspiration from robust alternatives like [dominate](https://github.com/Knio/dominate), PDOO emphasizes simplicity and ease of use.

With PDOO, you sidestep the need for clunky templating languages like Jinja or Mustache. Styling becomes a breeze using Python alone — no separate CSS files to juggle, just straightforward dynamic styling with f-strings.

Below is an example of the library in action. Note, the example below demonstrates **all** the concepts provided by PDOO. Scroll down below for a _gentler_ introduction to the library...

### Python
```python
from pdoo import Document, style

# Create the HTML document object
doc = Document()

# Create a dynamic CSS class that is parameterized by
# border_radius and background_color arguments.
@style
def style_fn(*, background_color, border_radius = 0):
    return lambda clsname: f"""
        .{clsname} {{
            background-color: {background_color};
            border-radius: {border_radius}px;
        }}
    """

# Begin defining the contents of the <head> tag.
with doc.head:
    # Create a <title> tag.
    with doc.tag("title"):
        # Inside the title tag, add the actual title text.
        doc.text("PDOO isn't too bad")

    # Now lets create a <script> tag.
    with doc.tag("script"):
        # As before, we want to include this JS code inside the script tag
        # however, we use "doc.raw" instead of "doc.text" to prevent escaping
        # of any HTML characters (i.e. "<" or ">").
        doc.raw("console.log(\"<hello world>\");")

# Now lets work on the <body>.
with doc.body:
    # As a shortcut, text can be provided directly as an argument
    # after the tag attributes...
    doc.tag("h1", {}, "Here are some custom labels")

    # Create a green label with square borders
    div_cls = doc.style(style_fn(background_color = "green"))
    with doc.tag("div", {"class": div_cls}):
        doc.text("This is green with square borders")

    # Create a blue label with round borders
    div_cls = doc.style(style_fn(background_color = "blue", border_radius = 4))
    with doc.tag("div", {"class": div_cls}):
        doc.text("This is blue with round borders")

    # Create a blue label with round borders
    div_cls = doc.style(style_fn(background_color = "blue", border_radius = 4))
    with doc.tag("div", {"class": div_cls}):
        doc.text("This is blue with round borders")

# Spit out the HTML!
print(str(doc))
```

### Output

```html
<!DOCTYPE html>
<html>
    <head>
        <style>
            .cls-__main__-style_fn-0 {
                background-color: green;
                border-radius: 0px;
            }
            .cls-__main__-style_fn-1 {
                background-color: blue;
                border-radius: 4px;
            }
        </style>
        <title>
            PDOO isn&#x27;t too bad
        </title>
        <script>
            console.log("<hello world>");
        </script>
    </head>
    <body>
        <h1>
            Here are some custom labels
        </h1>
        <div class="cls-__main__-style_fn-0">
            This is green with square borders
        </div>
        <div class="cls-__main__-style_fn-1">
            This is blue with round borders
        </div>
        <div class="cls-__main__-style_fn-1">
            This is blue with round borders
        </div>
    </body>
</html>
```

# Installation

You can install pdoo using `pip` via:

```bash
pip install pdoo
```

## Testing

You can test pdoo via:

```bash
python -m unittest discover -s test
```

# Usage

All code snippets below assume that both `Document` and `style` have been imported from `pdoo`:

```python
from pdoo import Document, style
```

## Getting started

To begin our journey with PDOO, we must first create an HTML Document. This is as simple as doing:

```python
# By default, PDOO will indent HTML by 4 spaces.
doc = Document(indent_prefix = 4)
print(str(doc))
```

This will generate a bare-bones empty HTML document with empty `<head>` and `<body>` tags:

```html
<!DOCTYPE html>
<html>
    <head>
        <style>
        </style>
    </head>
    <body>
    </body>
</html>
```

## Tags

Lets start adding to the `<body>` tag of our document. Adding content to a tag is as simple as "binding" it using python's `with` statement and then calling either:
  - `doc.tag` to append an HTML tag.
  - `doc.text` to append HTML-escaped text to the node.
  - `doc.raw` to append un-escaped HTML to the node

As we can see in the example below, tags created by `doc.tag` can themselves be bound using the `with` statement.

```python
doc = Document()
with doc.body:
    with doc.tag("div"):
        doc.text("Hello, World")
print(str(doc))
```

The above code generates the following HTML:

```html
<!DOCTYPE html>
<html>
    <head>
        <style>
        </style>
    </head>
    <body>
        <div>
            Hello, World
        </div>
    </body>
</html>
```

## Attributes

Similar to how tags, text and raw HTML can be added to a node, we can also add attributes. This can be done in two ways. First, we can pass a dictionary of `attribute_name : attribute_value` pairs as the second argument to `doc.tag`:

```python
doc.tag("div", {"id": "foobar", "class": "my-class" })
```

Alternatively, we can insert attributes to the currently bound tag by using the `doc.attr` method:
```python
with doc.tag("div"):
    doc.attr("id", "foobar")
    doc.attr("class", "my-class")
```

## Text

As seen in the "Tags" section above, text can be added to the currently bound tag by calling `doc.text`. Alternatively, we can pass in text as the third argument to `doc.tag` (after the attributes dictionary):

```python
doc.tag("div", {}, "Hello, World")
```

## Styling

PDOO allows us to remain in python even when styling our HTML components. PDOO keeps track of defined styles and generates unique class names that are guaranteed not to collide. PDOO also ensures that styles aren't redundantly redefined multiple times, ensuring file sizes are kept as small as possible!

To start styling with PDOO, lets first create a styling function:

```python
@style
def padding(padding_amount):
    return lambda cls: f"""
        .{cls} {{ padding: {padding_amount}px; }}
    """
```

A styling function takes some set of arguments and returns a **lambda** that itself generates CSS. This lambda is then passed the class name that PDOO generates for us to render a valid fragment of CSS that is included within an in-line `<style>` tag inside our `<head>`.

The reason why we use the approach of explicitly passing the class name into a lambda is that it makes more complex CSS a breeze to implement as shown below:

```python
@style
def responsive_padding(padding_amount, breakpoint):
    return lambda cls: f"""
        .{cls} {{ padding: {padding_amount}px; }}
        .{cls}:hover {{ color: red; }}
        @media (max-width: {breakpoint}px) {{
            .{cls} {{ display: none; }}
        }}
    """
```

To use a style function, we simply call it and pass the result to `doc.style`. We can then style a tag by assigning the result to the class attribute of a tag:

```python
class_name = doc.style(padding(6))
doc.text("div", {"class": class_name}, "I am a styled tag!" )
```

N.B. the `@style` decorator is required when creating a styling function as this facilitates the caching of identical styles, preventing the same styles being created multiple times under different class names.

## Components

If you've made it this far, congratulations! You understand _all_ of what PDOO has to offer. This last chapter doesn't introduce any new concepts, but instead demonstrates a powerful usage pattern that allows the creation of modular, re-usable components (A familiarity with `contextlib.contextmanager` is helpful).

Lets pretend we have a bunch of content on our website that we want to pad. One way we could do this is by styling each bit of content explicitly using a styling function. This is a bit of a faff - lets instead create a re-usable `padding` component which will automatically wrap any content in some padding.

First, lets create the styling function. We might want to pad the content by a variable amount so lets leave the padding amount as an input variable vs. hardcoding it:

```python
@style
def padding_style(padding_amount):
    return lambda cls: f"""
        .{cls} {{ padding: {padding_amount}px; }}
    """
```

Now lets create our padding component. All we must do is:

```python
@contextmanager
def padding_component(doc, *, padding_amount):
    cls = doc.style(padding_style(padding_amount))
    with doc.tag("div", {"class": cls}):
        yield
```

By constructing the component using the `@contextmanager` decorator, we can "bind" it in the same way we bind regular tags. Lets see the whole code in action:

```python
from pdoo import Document, style
from contextlib import contextmanager

@style
def padding_style(padding_amount):
    return lambda cls: f"""
        .{cls} {{ padding: {padding_amount}px; }}
    """

@contextmanager
def padding_component(doc, *, padding_amount):
    cls = doc.style(padding_style(padding_amount))
    with doc.tag("div", {"class": cls}):
        yield

# Create the HTML document object
doc = Document()
with doc.body:
    with padding_component(doc, padding_amount = 5):
        doc.text("Hello - I am padded by 5 pixels")
    with padding_component(doc, padding_amount = 5):
        with padding_component(doc, padding_amount = 5):
            doc.text("Hello - I am padded by 10 pixels")

print(str(doc))
```

This generates the following HTML:

```html
<!DOCTYPE html>
<html>
    <head>
        <style>
            .cls-__main__-padding_style-0 { padding: 5px; }
        </style>
    </head>
    <body>
        <div class="cls-__main__-padding_style-0">
            Hello - I am padded by 5 pixels
        </div>
        <div class="cls-__main__-padding_style-0">
            <div class="cls-__main__-padding_style-0">
                Hello - I am padded by 10 pixels
            </div>
        </div>
    </body>
</html>
```

As you can see, its quite straight-forward to create modular components that can be re-used and composed together across your code-base!

## Appendix: Asynchronous python

_tl;dr this library works well with async web frameworks_

This library requires tags, text and raw HTML to be created via methods on the `Document` object. As a result, the document (Usually named `doc`) needs to be explicitly passed around. This might feel like sub-par UX however it was a conscious choice - it means that currently bound tags are not stored under global variables but instead are stored in the document.

This means that this library plays nice with asynchronous web frameworks like [sanic](https://github.com/sanic-org/sanic), as concurrent requests won't interfere with one another - one request can't affect the currently bound tag of another. 

An alternate approach might be to use a `contextlib.ContextVar` to store currently bound tags. This would free us from having to pass `doc` everywhere - However, I want to avoid "magic" as much as possible. Although the current UX is slightly clunkier then it needs to be, its dead simple to understand and I intend to keep it as such.

## Thanks

Thanks for reading fellas! If you have any questions/suggestions, please reach out. My details are as follows:

  - Email: [t@lonny.io](mailto:t@lonny.io)
  - Website: [The Lonny Corporation](https://lonny.io)
