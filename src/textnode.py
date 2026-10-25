from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    PLAIN_TEXT = "plaintext"
    BOLD_TEXT = "boldtext"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "codetext"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self,other):
        return (self.text == other.text and self.text_type == other.text_type and
                self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN_TEXT:
        return LeafNode(tag=None,value=text_node.text,props=None)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag="b",value=text_node.text,props=None)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag="i",value=text_node.text,props=None)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code",value=text_node.text,props=None)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a",value=text_node.text,props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(tag="img",value="",props={"src":text_node.url,"alt":text_node.text})
    else:
        raise Exception("text node must be one of these types")


