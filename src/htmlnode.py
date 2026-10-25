class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
       raise NotImplementedError("to_html method not implemented") 
    def props_to_html(self):
        result=""
        if self.props == None or self.props == "":
            return ""
        for key in self.props:
            result += f' {key}="{self.props[key]}"'
        return result
    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag=tag,value=value,children=[],props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,value=None,children=children,props=props)
    def to_html(self):
        result = ""
        if self.tag is None:
            raise ValueError("object must have a tag")
        if self.children is None:
            raise ValueError("children missing a value")
        for child in self.children:
            result+=child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
