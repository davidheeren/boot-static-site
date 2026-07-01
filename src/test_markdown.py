
import unittest

from textnode import TextNode, TextType
from markdown_helper import split_nodes_delimiter


class TestMarkdown(unittest.TestCase):
    def test_split_nodes1(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        compare_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes2(self):
        node = TextNode("This is text with a **bold word** and _italic word_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        compare_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold word", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic word", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes3(self):
        node = TextNode("This is text with a **bold word** and another **bold word**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        compare_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold word", TextType.BOLD),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("bold word", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, compare_nodes)
