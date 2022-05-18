import sys
import os

from rich.console import Console

from utils.database_init import database_init
from utils.md_init import md_init
from tui.tui import main_ui


def main(scp_num):
    sys.path.append("..")

    main_ui()

    if not os.path.isfile("database/fetch"):
        database_init()

    main_md = md_init(scp_num)
    if not main_md:
        md_init(scp_num)
