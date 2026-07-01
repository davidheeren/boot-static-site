
import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    results = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            results.append(node)
            continue
        parts = node.text.split(delimiter)
        if (len(parts) % 2 == 0):
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
            if (len(parts) < 2):
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
            if (len(parts) < 2):
                raise ValueError("Cannot split on link")
            if parts[0]:
                results.append(TextNode(parts[0], TextType.PLAIN))
            remaining_text = parts[1]
            results.append(TextNode(anchor, TextType.LINK, url))
        if remaining_text:
            results.append(TextNode(remaining_text, TextType.PLAIN))
    return results


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
