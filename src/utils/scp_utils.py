import os
import sys
from time import process_time

import requests
from bs4 import BeautifulSoup as bs
from random_user_agent.user_agent import UserAgent
from rich.console import Console


class Utils:
    sys.path.append("..")
    console = Console()

    def __init__(self):
        pass

    def scp_search(self, scp_num):
        user_agent = UserAgent()

        start_time = process_time()
        link = f"https://the-scp.foundation/object/scp-{scp_num}"

        try:
            with self.console.status(
                    "[bold turquoise4][=] Checking access to database ...[/bold turquoise4]",
                    spinner="bouncingBar"
                ):
                header = {"User-Agent": user_agent.get_random_user_agent()}
                response = requests.get(link, headers=header)

                if response.status_code not in list(range(200, 299)):
                    raise ConnectionError
        except ConnectionError:
            self.console.log(
                "[bold red][-] Database is offline, cannot initiate.[/bold red]"
            )
        else:
            with self.console.status(
                    "[bold turquoise4][=] Fetching anomaly's information ...[/bold turquoise4]",
                    spinner="bouncingBar"
                ):
                with open("database/anomalies.list", "a", encoding="utf-8") as anomalies:
                    anomalies.write(f"SCP-{scp_num}: {link}\n")

                    self.console.log(
                        f"[turquoise4]> Fetching data of [turquoise4][cyan]SCP-{scp_num}[/cyan]"
                    )

                    # fetch the html from the page
                    new_header = {"User-Agent": user_agent.get_random_user_agent()}
                    scp_data = requests.get(link, headers=new_header)
                    soup = bs(scp_data.content, "html5lib")

                    if scp_data.status_code in list(range(200, 299)):
                        self.console.log(
                            f"[turquoise4]> Metadata of [/turquoise4][cyan]SCP-{scp_num}[/cyan]"
                            + "[turquoise4] fetched, writing to database ...[/turquoise4]"
                        )
                        with open(
                                f"database/anomalies.list.d/scp_{scp_num}.info",
                                "w", encoding="utf-8"
                            ) as scp_info:
                            scp_info.write(soup.prettify())

                        self.console.log(
                            f"[green][+] Data of [/green][cyan]SCP-{scp_num}[/cyan]"
                            + "[green] written successfully to database.[/green]"
                        )
                    else:
                        self.console.log(
                            f"[red][-] Skipping [/red][cyan]SCP-{scp_num}[/cyan]"
                            + "[red], connection error.[/red]"
                        )

                end_time = process_time()
                self.console.log(
                    "[bold][green][+] Database initiated with total time of:[/green]"
                    + f"[cyan]{end_time-start_time}m[/cyan][/bold]"
                )

    def scp_list(self):
        if os.path.isfile("database/anomalies.list"):
            with open("database/anomalies.list", "r", encoding="utf-8") as scp_list:
                entries = scp_list.readlines()

        with self.console.status(
                "[bold turquoise4][=] Listing all entries ...[/bold turquoise4]"
            ):
            for entry in entries:
                info = entry.split(":")
                link = ''.join(info[1:]).replace('\n', '')
                self.console.log(
                    f"[turquoise4]> [/turquoise4][cyan]{info[0]}[/cyan]@[cyan]{link}[/cyan]"
                )
        self.console.log(
            f"[bold green][+] There are total of {len(entries)}"
            + " anomalies in the local database.[/bold green]\n"
            + "[bold][?] There anomalies are located at "
            + "[cyan]database/anomalies.list/:database/proc.anomalies.d/[/cyan][/bold]"
        )
