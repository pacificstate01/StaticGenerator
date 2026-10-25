import unittest
from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import extract_markdown_images, extract_markdown_links
from split_nodes_image import split_nodes_image
from split_nodes_link import split_nodes_link
from text_to_textnodes import text_to_textnodes
from markdown_to_blocks import markdown_to_blocks, BlockType, block_to_block_type
from markdown_to_html_node import markdown_to_html_node

class TestTextNode(unittest.TestCase):
    
    # ==================== TextNode Tests ====================
    def test_eq(self):
        """Test TextNode equality"""
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
        
    def test_neq(self):
        """Test TextNode inequality"""
        node = TextNode("ah marone", TextType.ITALIC_TEXT)
        node2 = TextNode("puttaza", TextType.PLAIN_TEXT)
        self.assertNotEqual(node, node2)
    
    # ==================== HTMLNode / LeafNode Tests ====================
    def test_leaf_to_html_p(self):
        """Test LeafNode paragraph conversion to HTML"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        """Test LeafNode anchor conversion to HTML with props"""
        node = LeafNode("a", "click me!", {"href": "https://www.google.com"})
        assert node.to_html() == '<a href="https://www.google.com">click me!</a>'
    
    # ==================== HTMLNode / ParentNode Tests ====================
    def test_to_html_with_children(self):
        """Test ParentNode with single child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_grandchildren(self):
        """Test ParentNode with nested children"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    # ==================== text_node_to_html_node Tests ====================
    def test_text(self):
        """Test plain text conversion to HTML"""
        node = TextNode("this is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a text node")
        
    def test_link(self):
        """Test link conversion to HTML"""
        node = TextNode("boot.dev", TextType.LINKS, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
    
    # ==================== split_nodes_delimiter Tests ====================
    def test_backticks(self):
        """Test splitting nodes with backtick delimiter (code)"""
        node = TextNode("this is some `code` right here", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(result, [
            TextNode("this is some ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" right here", TextType.PLAIN_TEXT),
        ])
        
    def test_bold(self):
        """Test splitting nodes with bold delimiter"""
        node = TextNode("this is some **bold text** right here", TextType.PLAIN_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(result, [
            TextNode("this is some ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" right here", TextType.PLAIN_TEXT),
        ])
    
    # ==================== inline_markdown Tests ====================
    def test_extract_markdown_images(self):
        """Test extracting markdown images"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        """Test extracting markdown links"""
        matches = extract_markdown_links(
            "this is a link dude [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com")
        ], matches)
    
    # ==================== split_nodes_image Tests ====================
    def test_split_images(self):
        """Test splitting nodes with images"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    # ==================== text_to_textnodes Tests ====================
    def test_to_textnodes(self):
        """Test full text-to-textnodes conversion with mixed inline elements"""
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ], new_nodes,)
    
    # ==================== markdown_to_blocks Tests ====================
    def test_markdown_to_blocks(self):
        """Test splitting markdown into blocks"""
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    # ==================== block_to_block_type Tests ====================
    def test_block_paragraph(self):
        """Test identifying paragraph block type"""
        block = "some example markdown text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_heading(self):
        """Test identifying heading block type"""
        block = "### some example markdown text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_block_quote(self):
        """Test identifying quote block type"""
        block = ">some example markdown text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_ordered(self):
        """Test identifying ordered list block type"""
        block = "1. some example markdown text\n2. lista\n3. poto"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        
    def test_block_unordered(self):
        """Test identifying unordered list block type"""
        block = "- some example markdown text\n- peo"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_code(self):
        """Test identifying code block type"""
        block = "```\nsome example markdown text ```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    # ==================== markdown_to_html_node Tests ====================
    def test_paragraphs(self):
        """Test converting paragraphs to HTML"""
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """Test converting code blocks to HTML"""
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
if __name__ == "__main__":
    unittest.main()
