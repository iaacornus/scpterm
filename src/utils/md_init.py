import sys
import os
import re
from time import process_time

from rich.console import Console

from utils.scp_utils import Utils


def md_init(scp_num):
    console = Console()
    utils = Utils()

    start_time = process_time()
    ANOMALIES_PATH = "database/proc.anomalies.d"
    sys.path.append("..")

    if not os.path.isfile(f"{ANOMALIES_PATH}/scp_{scp_num}.md"):
        if not os.path.exists(ANOMALIES_PATH):
            console.print(">>> Creating file for decoded data ...")
            os.mkdir(ANOMALIES_PATH)

        check, soup = utils.fetch_soup(scp_num),
        try:
            for _ in range(3):
                ans = console.input(
                        f"[bold]> Check [cyan]SCP-{scp_num}[/cyan] in"
                        + "online database? [/bold]"
                    ).lower()
                if "y" in ans:
                    utils.scp_search(scp_num)
                    check, soup = utils.fetch_soup(scp_num)

                    if check:
                        break
                    else:
                        continue
                raise ConnectionError
        except ConnectionError:
            raise SystemExit
        else:
            pass

        with console.status(
                "[bold][>] Decoding the file ...[/bold]", spinner="bouncingBar"
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
                            "div", {
                                    "class": "scp-special-containment-procedures"
                                }
                        )
                        if not (
                                re.search(
                                        "scp-image-block block-right",
                                        str(extr)
                                    )
                                or re.search(
                                        "special-containment-procedures",
                                        str(extr)
                                    )
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
                    f"ANOMALIES_PATH/scp_{scp_num}.md",
                    "w",
                    encoding="utf-8"
                ) as proc_scp_info:
                proc_scp_info.write(
                    f"# {scp_code} ({scp_name})\n"
                    + f"**Classification:** {scp_class}\n"
                    + f"\n_Further classification:_ {scp_classifications}\n"
                    + "## Special Containment Procedures\n"
                    + f"{' '.join(list(scp_cp))}\n"
                    + f"## SCP Description\n{scp_description}\n"
                )

        end_time = process_time()
        console.print(
            "[bold green][+] Data decoded successfully.[/bold green]"
            + f"\Annomaly: [cyan]{scp_code}, {scp_name}[/cyan]"
            + f"\nElapsed time: [cyan]{end_time-start_time}[/cyan]."
        )

    print("\033c") # clear the terminal
    utils.view_md(scp_num)
    utils.view_img(scp_num)
