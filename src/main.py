from copystatic import recursive_copy
import os
from generate_pages import generate_pages_recursive
import sys
def main():

    recursive_copy("static","docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive("content", "template.html", "docs",basepath)
if __name__ == "__main__":
    main()
