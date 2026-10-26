import os

from markdown_to_html_node import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for c in lines:
        if c.startswith("# "):
            word = c[2:]
            word = word.strip(" ")
            return word
        
    raise Exception("not found")

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path,"r")
    content = f.read()
    f.close()
    f2 = open(template_path,"r")
    template = f2.read()
    f2.close()
    contents = markdown_to_html_node(content)
    page = contents.to_html()
    title = extract_title(content)
    text = template.replace("{{ Title }}",title)
    text = text.replace("{{ Content }}",page)
    text = text.replace('href="/',f'href="{basepath}')
    text = text.replace('src="/',f'src="{basepath}')
    folder = os.path.dirname(dest_path)
    os.makedirs(folder, exist_ok=True)
    f = open(dest_path,"w")
    f.write(text)
    f.close()