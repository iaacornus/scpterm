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
    init = True

    start_time = process_time()
    link = "https://the-scp.foundation/"

    if os.path.isfile("database/fetch"):
        with open("database/fetch", "r", encoding="utf-8") as data:
            data_info = data.readlines()

        if re_init:
            if "y" in console.input(
                    "[bold][:] Database already exists (last fetch:"
                    + f"[cyan]{data_info[1]}[/cyan]). Re-initiate? [/bold]"
                ).lower():
                for root, _, files in os.walk("database"):
                    for file in files:
                        os.remove(os.path.join(root, file))

                console.log(
                    "[bold green][+] Database removed, re-initiating ...[/bold green]"
                )
            else:
                console.log("[bold red][-] Process aborted.[/bold red]")
                raise SystemExit
        else:
            console.log(
                "[bold][?] Database already exists (last fetch:"
                + f"[cyan]{data_info[1]}[/cyan]).[/bold]"
            )
            init = False

    if init:
        try:
            utils.check_status(link, user_agent.get_random_user_agent())
        except ConnectionError:
            console.log(
                "[bold red][-] Database is offline, cannot initiate.[/bold red]"
            )
        else:
            console.log(
                "[bold red][^] Some of the anomalies would not be fetched "
                + "due to classified reason.[/bold red] Press any key to continue."
            )
            input()

            with open("database/fetch" ,"w", encoding="utf-8") as data:
                data.write(f"Fetched data:\n{time.now().strftime('%d:%m/%H:%M:%S')}")

            if not os.path.exists("database/anomalies.list.d"):
                console.log(
                    "[turquoise4]> Creating directory for data of anomalies ...[/turquoise4]"
                )
                os.mkdir("database/anomalies.list.d")

            with console.status(
                "[bold turquoise4][=] Fetching anomalies information ...[/bold turquoise4]",
                spinner="bouncingBar"
            ):
                with open("database/anomalies.list", "a", encoding="utf-8") as anomalies:
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
                            f"[turquoise4]> Fetching data: [turquoise4][cyan]SCP-{scp_num}[/cyan]"
                        )

                        # fetch the html from the page
                        new_header = {"User-Agent": user_agent.get_random_user_agent()}
                        scp_data = requests.get(scp_link, headers=new_header)
                        soup = bs(scp_data.content, "html5lib")

                        if scp_data.status_code in list(range(200, 299)):
                            console.log(
                                f"[turquoise4]> Metadata: [/turquoise4][cyan]SCP-{scp_num}[/cyan]"
                                + "[turquoise4] fetched, writing to database ...[/turquoise4]"
                            )
                            with open(
                                    f"database/anomalies.list.d/scp_{scp_num}.info",
                                    "w", encoding="utf-8"
                                ) as scp_info:
                                scp_info.write(soup.prettify())

                            console.log(
                                f"[green][+] Data of [/green][cyan]SCP-{scp_num}[/cyan]"
                                + "[green] written successfully to database.[/green]"
                            )
                        else:
                            console.log(
                                f"[red][-] Skipping [/red][cyan]SCP-{scp_num}[/cyan]"
                                + "[red], connection error.[/red]"
                            )

                end_time = process_time()
                console.log(
                    "[bold][green][+] Database initiated with total time of:[/green]"
                    + f"[cyan]{end_time-start_time}m[/cyan][/bold]"
                )

