import sys
import os
from random import randint

import pytermgui as ptg
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align


def main_ui():
    sys.path.append("..")

    width, height = os.get_terminal_size()
    console = Console()

    while (width < 108) or (height < 32):
        try:
            panel = Panel(
                Align(
                    Text(
                        "Please resize your terminal.",
                        justify="center",
                        style="bold red"
                    ),
                    vertical="middle", align="center"
                ),
                width=width, height=(height-1)
            )
            console.print(panel)
            width, height = os.get_terminal_size()
        except KeyboardInterrupt:
            sys.stderr.write("\x1b[2J\x1b[H")
    else:
        with open(f"img/scp_logo.txt") as logo_ascii:
            logo = logo_ascii.read()

        time = 0
        while time < 5000:
            panel = Panel(
                Align(
                    Text(
                        f"{logo}\t\t\t\tLoading: {round((time/50)/(5000/50), 2)*100}%",
                        style="bold"
                    ),
                    vertical="middle", align="center"
                ),
                width=width, height=(height-1)
            )
            console.print(panel)
            time += randint(1, 7)

        sys.stderr.write("\x1b[2J\x1b[H")
