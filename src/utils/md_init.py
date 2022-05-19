import sys
import os
import re
from datetime import datetime as time
from time import process_time

from rich.console import Console

from utils.scp_utils import Utils


console = Console()
utils = Utils()


def md_init(scp_num):
    sys.path.append("..")

    start_time = process_time()

    if not os.path.isfile(f"database/proc.anomalies.d/scp_{scp_num}.md"):
        if not os.path.exists("database/proc.anomalies.d"):
            os.mkdir("database/proc.anomalies.d")

        (check, soup), trial = utils.fetch_soup(scp_num), 0
        while not check:
            utils.console.log(
                f"[red]> Failed attempt, try: {trial}[/red]"
            )
            if trial == 2:
                console.log(
                    "[bold red][-] Too many failed attempts, aborting.[/bold red]"
                )
                break
            if "y" in console.input(
                    f"[bold][:] Check [cyan]SCP-{scp_num}[/cyan] in online database? [/bold]"
                ).lower():
                utils.scp_search(scp_num)
                check, soup = utils.fetch_soup(scp_num)


        with console.status(
                "[bold turquoise4][=] Decoding the file ...[/bold turquoise4]",
                spinner="bouncingBar"
            ):
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

            with open(
                    f"database/proc.anomalies.d/scp_{scp_num}.md", "w", encoding="utf-8"
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

    print("\033c") # clear the terminal
    utils.view_md(scp_num)
    utils.view_img(scp_num)

    console.log(
        f"[bold][?] File location: [cyan]database/proc.anomalies.d/scp_{scp_num}.md[/cyan]"
    )
