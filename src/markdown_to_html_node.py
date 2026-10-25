from markdown_to_blocks import markdown_to_blocks,BlockType,block_to_block_type
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node,TextNode,TextType
from htmlnode import ParentNode
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        node = text_node_to_html_node(text_node)
        children.append(node)
    return children

def heading_to_html_node(block):
    count = 0 
    for i in block:
        if i == "#":
            count+=1
        else:
            break
    cleaned_block = block.strip("#").strip(" ")
    tag_string = f"h{count}"
    children = text_to_children(cleaned_block)
    return ParentNode(tag_string,children)

def paragraph_to_html_node(block):
    content = block
    content_replaced = content.replace("\n"," ")
    tag_string="p"
    children = text_to_children(content_replaced)
    return ParentNode(tag_string,children)


def code_to_html_node(block):
    content = block.strip("`")     
    content = content.lstrip("\n")
    text_node = TextNode(content, TextType.PLAIN_TEXT)
    code_html_node = text_node_to_html_node(text_node)
    parent_code = ParentNode("code", [code_html_node])
    return ParentNode("pre", [parent_code])

def quote_to_html_node(block):
    content= block.split("\n")
    content_quotes = []
    for line in content:
        content_quotes.append(line.strip(">").strip(" "))
    final_text = "\n".join(content_quotes)
    tag_string = "blockquote"
    children = text_to_children(final_text)
    return ParentNode(tag_string,children)

def unordered_to_html_node(block):
    content = block.split("\n")
    unordered_content = []
    for line in content:
        unordered_list = line.strip("-").strip(" ")
        convert = text_to_children(unordered_list)
        parent_unordered = ParentNode("li",convert)
        unordered_content.append(parent_unordered)
    tag_string = "ul"
    return ParentNode(tag_string,unordered_content)


def ordered_list_to_html_node(block):
    content = block.split("\n")
    ordered_list = []
    for i,line in enumerate(content,start=1):
        cleaned = line.removeprefix(f"{i}. ")
        children = text_to_children(cleaned)
        parent_ordered = ParentNode("li",children)
        ordered_list.append(parent_ordered)
    tag_string = "ol"
    return ParentNode(tag_string,ordered_list)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_htmlnodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
            child_htmlnodes.append(block_node)
        elif block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
            child_htmlnodes.append(block_node)
        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
            child_htmlnodes.append(block_node)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
            child_htmlnodes.append(block_node)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_to_html_node(block)
            child_htmlnodes.append(block_node)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)
            child_htmlnodes.append(block_node)
    return ParentNode("div",child_htmlnodes)