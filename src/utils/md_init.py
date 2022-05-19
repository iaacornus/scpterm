import sys
import os
import re
from datetime import datetime as time
from random import uniform
from time import sleep, process_time

from bs4 import BeautifulSoup as bs
from rich.markdown import Markdown
from rich.console import Console

from utils.scp_utils import Utils


console = Console()
utils = Utils()


def md_init(scp_num):
    sys.path.append("..")

    start_time = process_time()

    if os.path.isfile(f"database/proc.anomalies.d/scp_{scp_num}.md"):
        utils.view_md()
        with open(
            f"database/proc.anomalies.d/scp_{scp_num}.md"
        ) as scp_data:
            scp_md = Markdown(scp_data.read())

        console.print(scp_md)
    else:
        if not os.path.exists("database/proc.anomalies.d"):
            os.mkdir("database/proc.anomalies.d")

        if os.path.isfile(f"database/anomalies.list.d/scp_{scp_num}.info"):
            print("\033c") # clear the terminal
            with console.status(
                    "[bold turquoise4][=] Decoding the file ...[/bold turquoise4]",
                    spinner="bouncingBar"
                ):
                with open(
                        f"database/anomalies.list.d/scp_{scp_num}.info",
                        "r", encoding="utf-8"
                    ) as scp_info:
                    index = scp_info.read()
                    soup = bs(index, "html5lib")

                # begin extraction of data
                scp_code = f"SCP-{scp_num}"
                scp_name = soup.find("h2", {"class": "scp-nickname"}).text.strip()

                # class is the general classification of the scp
                scp_class = soup.find("div", {"class": "scp-tag"}).text.strip()
                scp_classifications = [ # while this one is the other classifications
                    fc.text.strip() for fc in list(
                        soup.find("aside", {"class": "scp-sidebar"})
                    )
                    if fc.text.strip() != ""
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

                scp_description = [ # scp description
                    fdesc.text.strip() for fdesc in list(
                        soup.find("div", {"class": "scp-description"})
                    )
                    if fdesc.text.strip() not in ["\n", ""]
                ][1]
                scp_img_dir = utils.fetch_img(soup, scp_num)

                with open(
                        f"database/proc.anomalies.d/scp_{scp_num}.md",
                        "w", encoding="utf-8"
                    ) as proc_scp_info:
                    proc_scp_info.write(
                        f"# {scp_code} ({scp_name})\n**Classification:** {scp_class}\n"
                        + f"\n_Further classification:_ {scp_classifications}\n"
                        + "## Special Containment Procedures\n"
                        + f"{' '.join(list(scp_cp))}\n"
                        + f"## SCP Description\n{scp_description}\n"
                    )

            end_time = process_time()
            console.log(
                "[bold green][+] Decoded successfully[/bold green]:"
                + f"\n[cyan]{scp_code}: {scp_name} @{time.now().strftime('%H:%M:%S')}"
                + f"\nElapsed time: {end_time-start_time}[/cyan]."
            )

        else:
            console.log(
                f"[bold][red][-] [/red][cyan]SCP-{scp_num}[/cyan][red] does not exist.[/red]"
            )
            if "y" in console.input(
                    f"[bold][:] Check SCP-{scp_num} in online database? [/bold]"
                ).lower():
                utils.scp_search(scp_num)

            return False

    console.log(
        f"[bold][?] File location: [cyan]database/proc.anomalies.d/scp_{scp_num}.md[/cyan]"
    )
