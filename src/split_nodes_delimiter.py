from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        pieces = node.text.split(delimiter)
        if len(pieces) % 2 == 0:
            raise Exception("invalid markdown, no closing delimiter")
        for i,piece in enumerate(pieces):
            if i % 2 == 0:
                new_nodes.append(TextNode(piece,TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(piece,text_type))
    return new_nodes



