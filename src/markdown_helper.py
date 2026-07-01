
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
