import unittest

from gencontent import extract_title


class TestGenerateContent(unittest.TestCase):
    def test_extract_title(self):
        md = """# hello """
        blocks = extract_title(md)
        self.assertEqual(
            blocks,"hello"
            
        )
    def test_extract_title_no_h1(self):
        md = """## no title"""  
        with self.assertRaises(Exception):
            extract_title(md)