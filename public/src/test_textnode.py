import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode,ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("ah marone", TextType.ITALIC_TEXT)
        node2 = TextNode("puttaza", TextType.PLAIN_TEXT)
        self.assertNotEqual(node,node2)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a","click me!",{"href": "https://www.google.com"})
        assert node.to_html() == '<a href="https://www.google.com">click me!</a>'
    def test_to_html_with_children(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode("div",[child_node])
        self.assertEqual(parent_node.to_html(),"<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        

if __name__ == "__main__":
    unittest.main()
