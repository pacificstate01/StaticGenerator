from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    newsplit = markdown.split("\n\n")
    filtered = []
    for line in newsplit:
        stripped = line.strip()
        if stripped != "":
            # Split into lines, strip each line, then rejoin
            lines = stripped.split("\n")
            cleaned_lines = [l.strip() for l in lines]
            filtered.append("\n".join(cleaned_lines))
    return filtered

def block_to_block_type(text):
    if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    lines = text.split("\n")
    if len(lines)>=2 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if text.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if text.startswith("- "):
        for unordered in lines:
            if not unordered.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if text.startswith("1. "):
        for i,line in enumerate(lines,start=1):
            expected_prefix = f"{i}. "
            if not line.startswith(expected_prefix):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
