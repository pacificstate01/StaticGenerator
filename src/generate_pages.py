import os
from gencontent import generate_page
from pathlib import Path
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for content in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content,content)
        dest_path = os.path.join(dest_dir_path,content)
        if os.path.isfile(full_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(full_path,template_path,dest_path)
        else:
            generate_pages_recursive(full_path,template_path,dest_path)
            