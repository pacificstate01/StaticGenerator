from copystatic import recursive_copy
import os
from generate_pages import generate_pages_recursive
def main():

    recursive_copy("static","public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
