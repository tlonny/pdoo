from unittest import TestCase
from textwrap import dedent
from pdoo import Document

class BasicFunctionalityTest(TestCase):

    def test_escaping(self):
        doc = Document()
        with doc.body:
            with doc.tag("div", {"foo": "\"<>"}):
                doc.attr("bar", "&&")
                doc.text("<>")
        self.assertEqual(str(doc), dedent("""
            <!DOCTYPE html>
            <html>
                <head>
                    <style>
                    </style>
                </head>
                <body>
                    <div foo="&quot;&lt;&gt;" bar="&amp;&amp;">
                        &lt;&gt;
                    </div>
                </body>
            </html>
        """).strip())

    def test_void(self):
        doc = Document()
        with doc.body:
            doc.tag("meta")
        self.assertEqual(str(doc), dedent("""
            <!DOCTYPE html>
            <html>
                <head>
                    <style>
                    </style>
                </head>
                <body>
                    <meta>
                </body>
            </html>
        """).strip())

