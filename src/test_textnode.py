import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("Test1", TextType.BOLD)
        node2 = TextNode("Test2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("Text", TextType.BOLD, "test.com")
        node2 = TextNode("Text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_convert_text_plain(self):
        node = TextNode("My text", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "My text")
        self.assertEqual(html_node.to_html(), "My text")

    def test_convert_text_bold(self):
        node = TextNode("My text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "My text")
        self.assertEqual(html_node.to_html(), "<b>My text</b>")

    def test_convert_text_italic(self):
        node = TextNode("My text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "My text")
        self.assertEqual(html_node.to_html(), "<i>My text</i>")

    def test_convert_text_code(self):
        node = TextNode("My text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "My text")
        self.assertEqual(html_node.to_html(), "<code>My text</code>")

    def test_convert_text_link(self):
        node = TextNode("Google link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google link")
        self.assertEqual(html_node.props["href"], "https://www.google.com")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Google link</a>')

    def test_convert_text_image(self):
        node = TextNode("Image link", TextType.IMAGE, "https://picsum.photos/200")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://picsum.photos/200")
        self.assertEqual(html_node.props["alt"], "Image link")
        self.assertEqual(html_node.to_html(), '<img src="https://picsum.photos/200" alt="Image link"></img>')


if __name__ == "__main__":
    unittest.main()
