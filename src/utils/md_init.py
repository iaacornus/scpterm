import sys
import os
import re
from datetime import datetime as time
from random import uniform
from time import sleep, process_time

import cv2 as cv
from rich.markdown import Markdown
from rich.console import Console
from bs4 import BeautifulSoup as bs


def data_search(scp_num):
    console = Console()

    if os.path.isfile(f"database/proc.anomalies.d/scp_{scp_num}.md"):
        print(chr(27) + "[2J") # clear the terminal
        console.log(
            f"[bold green][+] Decoded successfully[/bold green] @[cyan]{time.now().strftime('%H:%M:%S')}[/cyan]."
        )
        with console.status(
                f"[bold turquoise4][=] Opening decoded file ...[/bold turquoise4]"
            ):
            sleep(uniform(0.1, 5.0))
            with open(f"database/proc.anomalies.d/scp_{scp_num}.md") as scp_data:
                return Markdown(scp_data.read())
    else:
        return False


def md_init(scp_num):
    sys.path.append("..")

    start_time = process_time()
    console = Console()
    scp_check = data_search(scp_num)

    if not os.path.exists("database/proc.anomalies.d"):
        os.mkdir("database/proc.anomalies.d")

    if not scp_check:
        if os.path.isfile(f"database/anomalies.list.d/scp_{scp_num}.info"):
            print(chr(27) + "[2J") # clear the terminal
            with console.status(
                    f"[=] Decoding the file ...", spinner="bouncingBar"
                ):
                with open(
                        f"database/anomalies.list.d/scp_{scp_num}.info", "r"
                    ) as scp_info:
                    index = scp_info.read()
                    soup = bs(index, "html5lib")

                # begin extraction of data
                scp_code = f"SCP-{scp_num}"
                scp_name = soup.find("h2", {"class": "scp-nickname"}).text.strip()

                # class is the general classification of the scp
                scp_class = soup.find("div", {"class": "scp-tag"}).text.strip()
                scp_classifications = [ # while this one is the other classifications
                    fc.text.strip() for fc in [
                        c for c in soup.find(
                            "aside", {"class": "scp-sidebar"}
                        )
                    ] if fc.text.strip() != ""
                ]

                scp_cp = [ # special containment procedures
                    cp_text.text.strip() for cp_text in [
                        extr for extr in soup.find(
                            "div", {"class": "scp-special-containment-procedures"}
                        )
                        if not (
                                re.search("scp-image-block block-right", str(extr))
                                or re.search("special-containment-procedures", str(extr))
                            )
                    ]
                    if (cp_text.text.strip() not in ["\n", ""])
                ]

                scp_description = [
                    fdesc.text.strip() for fdesc in [
                        idesc for idesc in soup.find(
                            "div", {"class": "scp-description"}
                        )
                    ]
                    if fdesc.text.strip() not in ["\n", ""]
                ][1]
                reference = soup.find("p", {"id": "reference"}).text.strip().split("\n")[-1]

                with open(
                        f"database/proc.anomalies.d/scp_{scp_num}.md", "w"
                    ) as proc_scp_info:
                    proc_scp_info.write(f"# {scp_code} ({scp_name})\n")
                    proc_scp_info.write(f"**Classification:** {scp_class}")
                    proc_scp_info.write(f" ::_{' '.join([class_ for class_ in scp_classifications])}_\n")
                    proc_scp_info.write(f"## Special Containment Procedures\n")
                    proc_scp_info.write(f"{' '.join([items for items in scp_cp])}\n")
                    proc_scp_info.write(f"## SCP Description\n")
                    proc_scp_info.write(f"{scp_description}\n")
                    proc_scp_info.write(f"### References\n")
                    proc_scp_info.write(f"{reference}\n")

            end_time = process_time()
            console.log(
                f"[bold green][+] Decoded successfully[/bold green]:\n[cyan]{scp_code}: {scp_name} @{time.now().strftime('%H:%M:%S')}\nElapsed time: {end_time-start_time}[/cyan]."
            )
            with console.status(
                    f"[bold turquoise4][=] Opening decoded file ...[/bold turquoise4]"
                ):
                sleep(uniform(0.1, 5.0))
                with open(f"database/proc.anomalies.d/scp_{scp_num}.md") as scp_data:
                    scp_md =Markdown(scp_data.read())
                console.print(scp_md)

        else:
            console.log(
                f"[bold][red][-] [/red][cyan]SCP-{scp_num}[/cyan][red] does not exist.[/red]"
            )
            raise SystemExit
    else:
        console.print(scp_check)

    console.log(
        f"[bold][?] File location: [cyan]database/proc.anomalies.d/scp_{scp_num}.md[/cyan]"
    )
