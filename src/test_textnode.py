import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node3 = TextNode("Test1", TextType.BOLD)
        node4 = TextNode("Test2", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_not_eq_url(self):
        node5 = TextNode("Text", TextType.BOLD, "test.com")
        node6 = TextNode("Text", TextType.BOLD)
        self.assertNotEqual(node5, node6)


if __name__ == "__main__":
    unittest.main()
