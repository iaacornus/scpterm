import sys
import os
from time import process_time
from datetime import datetime as time

import requests
from bs4 import BeautifulSoup as bs
from random_user_agent.user_agent import UserAgent
from rich.console import Console

from utils.scp_utils import Utils


def database_init(re_init=False):
    sys.path.append("..")

    utils = Utils()
    console = Console()
    user_agent = UserAgent()

    DATABASE_PATH = "database/anomalies.list.d"

    init = True
    start_time = process_time()
    link = "https://the-scp.foundation/"

    if os.path.isfile("database/fetch"):
        with open("database/fetch", "r", encoding="utf-8") as data:
            data_info = data.readlines()

        if re_init:
            if "y" in console.input(
                    "[bold]> Database already exists (last fetch:"
                    + f"[cyan]{data_info[1]}[/cyan]). Re-initiate? [/bold]"
                ).lower():
                with console.status(
                        "[bold][>] Removing previous database ...[/bold]",
                        spinner="bouncingBar"
                    ):
                    for root, _, files in os.walk("database"):
                        for file in files:
                            console.print(f">>> Removing: {file}")
                            os.remove(os.path.join(root, file))
            else:
                console.print("[!] Process aborted.", style="bold red")
                raise SystemExit
        else:
            console.print(
                f"[*] Database last fetch: [cyan]{data_info[1]}[/cyan])."
            )
            init = False

    if init:
        try:
            utils.check_status(link, user_agent.get_random_user_agent())
        except ConnectionError:
            console.print(
                "[!] Database is offline, cannot initiate.", style="bold red"
            )
        else:
            console.input(
                "[*] Some of the anomalies would not be fetched due to"
                + "classified reason. Press any key to continue."
            )

            with open("database/fetch" ,"w", encoding="utf-8") as data:
                data.write(
                    f"Fetched data:\n{time.now().strftime('%d:%m/%H:%M:%S')}"
                )

            if not os.path.exists(DATABASE_PATH):
                console.log(
                    ">>> Creating directory for data of anomalies ..."
                )
                os.mkdir(DATABASE_PATH)

            with console.status(
                    "[bold][>] Fetching information of anomalies...[/bold]",
                    spinner="bouncingBar"
                ):
                with open(
                        "database/anomalies.list", "a", encoding="utf-8"
                    ) as anomalies:
                    for i in range(1, 1000):
                        if len(f"{i}") == 1:
                            scp_num = f"00{i}"
                        elif len(f"{i}") == 2:
                            scp_num = f"0{i}"
                        elif len(f"{i}") == 3:
                            scp_num = f"{i}"
                        scp_link = f"{link}/object/scp-{scp_num}"
                        anomalies.write(f"SCP-{scp_num}: {scp_link}\n")

                        console.log(
                            f">>> Fetching data: [cyan]SCP-{scp_num}[/cyan]"
                        )

                        # fetch the html from the page
                        new_header = {
                                "User-Agent": user_agent.get_random_user_agent()
                            }
                        scp_data = requests.get(scp_link, headers=new_header)
                        soup = bs(scp_data.content, "html5lib")

                        if scp_data.status_code in list(range(200, 299)):
                            console.log(
                                f"[*] Metadata: [cyan]SCP-{scp_num}[/cyan]"
                                + " fetched, writing to database ..."
                            )
                            with open(
                                    f"{DATABASE_PATH}/scp_{scp_num}.info",
                                    "w",
                                    encoding="utf-8"
                                ) as scp_info:
                                scp_info.write(soup.prettify())

                            console.print(
                                f"[green]+>> DATA: [/green]SCP-{scp_num}"
                                + f"[green] written in database [/green]"
                            )
                        else:
                            console.print(
                                f"[red]!>> Skipping [/red]SCP-{scp_num}"
                                + "[red], connection error.[/red]"
                            )

                end_time = process_time()
                console.print(
                    "[bold][=] Database initiated with total time of:"
                    + f"[cyan]{end_time-start_time}m[/cyan][/bold]"
                )

