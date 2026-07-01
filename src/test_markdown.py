
import unittest

from textnode import TextNode, TextType
from markdown_helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, \
    split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_split_nodes_image1(self):
        node = TextNode(
            "This is text with a link ![my image](https://i.imgur.com/zjjcJKZ.png). Thanks",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("my image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(". Thanks", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, compare_nodes)

    def test_split_nodes_image2(self):
        node = TextNode(
            "This is text with a link ![my image](https://i.imgur.com/zjjcJKZ.png) and ![my new image](https://i.imgur.com/test_image.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("my image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("my new image", TextType.IMAGE, "https://i.imgur.com/test_image.png"),
        ]
        self.assertListEqual(new_nodes, compare_nodes)

    def test_split_nodes_image3(self):
        node = TextNode(
            "This is text with a link ![my image](https://i.imgur.com/zjjcJKZ.png) and ![my image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("my image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("my image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(new_nodes, compare_nodes)

    def test_split_nodes_image4(self):
        node = TextNode(
            "This is text with no links",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        compare_nodes = [
            TextNode("This is text with no links", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, compare_nodes)

    def test_split_nodes_link1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_link2(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_link3(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_link4(self):
        node = TextNode(
            "This is text with no link",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        compare_nodes = [
            TextNode("This is text with no link", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_link5(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        compare_nodes = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_both1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_both2(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        compare_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_split_nodes_both3(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        compare_nodes = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_text_to_nodes1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        compare_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_text_to_nodes2(self):
        text = "This is **text** with an _italic_ word and a `code block` and more **bold** and more _italic_ and more `code` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        compare_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and more ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and more ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and more ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, compare_nodes)

    def test_text_to_nodes3(self):
        text = "_Here_ we have **two** of the same images: ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg). `Isn't that cool?`"
        new_nodes = text_to_textnodes(text)
        compare_nodes = [
            TextNode("Here", TextType.ITALIC),
            TextNode(" we have ", TextType.PLAIN),
            TextNode("two", TextType.BOLD),
            TextNode(" of the same images: ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(". ", TextType.PLAIN),
            TextNode("Isn't that cool?", TextType.CODE),
        ]
        self.assertEqual(new_nodes, compare_nodes)
