import unittest

from htmlnode import HTMLNode, LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_propts_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("mytag", "myvalue")
        self.assertEqual(repr(node), "tag: mytag, value: myvalue, children: None, props: None")

    def test_repr2(self):
        node = HTMLNode("mytag", "myvalue", [], {"target": "_blank"})
        self.assertEqual(repr(node), "tag: mytag, value: myvalue, children: [], props: {'target': '_blank'}")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>',)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
