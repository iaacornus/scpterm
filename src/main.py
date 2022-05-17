import sys
sys.path.append("..")

from rich.console import Console
from rich.markdown import Markdown

from misc.colors import Colors

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())

console.print(markdown)


def main():
    pass
