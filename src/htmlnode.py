
# allow type annotations for own type
from __future__ import annotations


class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Must supply a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, props: {self.props}"
