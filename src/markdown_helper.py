import re
from enum import Enum

from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            results.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, delimiter not closed")
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                results.append(TextNode(part, TextType.PLAIN))
            else:
                results.append(TextNode(part, text_type))
    return results


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            results.append(node)
            continue
        image_links = extract_markdown_images(node.text)
        # in case we have two of the same exact links
        remaining_text = node.text
        for anchor, url in image_links:
            parts = remaining_text.split(f"![{anchor}]({url})", 1)
            if len(parts) < 2:
                raise ValueError("Cannot split on image link")
            if parts[0]:
                results.append(TextNode(parts[0], TextType.PLAIN))
            remaining_text = parts[1]
            results.append(TextNode(anchor, TextType.IMAGE, url))
        if remaining_text:
            results.append(TextNode(remaining_text, TextType.PLAIN))
    return results


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            results.append(node)
            continue
        links = extract_markdown_links(node.text)
        remaining_text = node.text
        for anchor, url in links:
            parts = remaining_text.split(f"[{anchor}]({url})", 1)
            if len(parts) < 2:
                raise ValueError("Cannot split on link")
            if parts[0]:
                results.append(TextNode(parts[0], TextType.PLAIN))
            remaining_text = parts[1]
            results.append(TextNode(anchor, TextType.LINK, url))
        if remaining_text:
            results.append(TextNode(remaining_text, TextType.PLAIN))
    return results


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    return [b.strip() for b in markdown.split("\n\n")]


def block_to_block_type(block: str) -> BlockType:
    # [\s\S] means match all including new lines
    if re.match(r"^#{1,6} .*$", block):
        return BlockType.HEADING
    if re.match(r"^```\n[\s\S]*```$", block):
        return BlockType.CODE

    lines = block.split("\n")

    def is_quote():
        for line in lines:
            if not re.match(r"^>", line):
                return False
        return True

    def is_unordered_list():
        for line in lines:
            if not re.match(r"^- ", line):
                return False
        return True

    def is_ordered_list():
        for i, line in enumerate(lines):
            if not re.match(rf"^{i+1}\. ", line):
                return False
        return True

    if (is_quote()):
        return BlockType.QUOTE
    if (is_unordered_list()):
        return BlockType.UNORDERED_LIST
    if (is_ordered_list()):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def extract_markdown_images(text):
    # example: ![rick roll](https://i.imgur.com/aKaOqIh.gif)
    # pattern = r"!\[(.+?)\]\((.+?)\)" # my first attempt
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    # example: [to boot dev](https://www.boot.dev)
    # pattern = r"(?<!!)\[(.+?)\]\((.+?)\)" # my first attempt
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
