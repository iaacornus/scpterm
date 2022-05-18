import sys
import os
from random import uniform

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
            print("\033c")
    else:
        with open(f"img/scp_logo.txt") as logo_ascii:
            logo = logo_ascii.read()

        time = 0
        while time < 5000:
            percent = round((time/50)/(5000/50), 2)*100
            stages = [uniform(0.0, 100.0) for n in range(4)]
            stages.sort()

            if percent < stages[0]:
                process = "[=] Accessing database ..."
            elif percent < stages[1]:
                process = "[=] Searching for entry ..."
            elif percent < stages[2]:
                process = "[=] Collecting files of entry ..."
            elif percent < stages[3]:
                process = "[=] Preparing collected data ..."

            panel = Panel(
                Align(
                    Text(
                        f"{logo}\t\t\t{process}: {percent}%",
                        style="bold"
                    ),
                    vertical="middle", align="center"
                ),
                width=width, height=(height-1)
            )
            console.print(panel)
            time += uniform(0.1, 7.0)

