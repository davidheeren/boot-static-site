
import unittest

from textnode import TextNode, TextType
from markdown_helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

    def test_parse_image1(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_parse_image2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)

    def test_parse_image3(self):
        matches = extract_markdown_images("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    def test_parse_image4(self):
        matches = extract_markdown_images("This is text with an ![[]()")
        self.assertListEqual([], matches)

    def test_parse_link1(self):
        matches = extract_markdown_links("This is text with an [google](https://google.com)")
        self.assertListEqual([("google", "https://google.com")], matches)

    def test_parse_link2(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)

    def test_parse_link3(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    def test_parse_link4(self):
        matches = extract_markdown_links("This is text with an [](()")
        self.assertListEqual([], matches)
