import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
