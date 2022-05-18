import sys
sys.path.append("..")

import os
from time import process_time
from datetime import datetime as time

import requests
from random_user_agent.user_agent import UserAgent
from bs4 import BeautifulSoup as bs
from rich.console import Console

def database_init():
    console = Console()
    user_agent = UserAgent()

    start_time = process_time()
    link = "https://the-scp.foundation/object"

    if os.path.isfile("database/fetch"):
        with open("database/fetch", "r") as data:
            data_info = data.readlines()

        console.log(
            f"[bold][+] Database already exists (last fetch:[cyan]{data_info[1]}[/cyan]).[/bold]"
        )
    else:
        try:
            with console.status(
                "[bold turquoise4][=] Checking access to database ...[/bold turquoise4]",
                spinner="bouncingBar"
            ):
                header = {"User-Agent": user_agent.get_random_user_agent()}
                response = requests.get(link, headers=header)
        except ConnectionError:
            console.log(
                "[bold red][-] Database is offline, cannot initiate[/bold red]"
            )
        else:
            console.log(
                "[bold red][^] Some of the anomalies would not be fetched due to classified reason.[/bold red] Press any key to continue."
            )
            input()

            with open("database/fetch" ,"w") as data:
                data.write(f"Fetched data:\n{time.now().strftime('%d:%m/%H:%M:%S')}")

            if not os.path.exists(f"database/anomalies.list.d"):
                console.log(
                    "[turquoise4]> Creating directory for anomalies data ...[/turquoise4]"
                )
                os.mkdir(f"database/anomalies.list.d")

            with console.status(
                "[bold turquoise4][=] Fetching anomalies information ...[/bold turquoise4]",
                spinner="bouncingBar"
            ):
                with open("database/anomalies.list", "a") as anomalies:
                    for i in range(1, 1000):
                        if len(f"{i}") == 1:
                            scp_num = f"00{i}"
                        elif len(f"{i}") == 2:
                            scp_num = f"0{i}"
                        elif len(f"{i}") == 3:
                            scp_num = f"{i}"
                        scp_link = f"{link}/scp-{scp_num}"
                        anomalies.write(f"SCP-{scp_num}: {scp_link}\n")

                        console.log(
                            f"[turquoise4]> Fetching [turquoise4][cyan]SCP-{scp_num}[/cyan]"
                        )

                        # fetch the html from the page
                        new_header = {"User-Agent": user_agent.get_random_user_agent()}
                        scp_data = requests.get(scp_link, headers=new_header)
                        soup = bs(scp_data.content, "html5lib")

                        if scp_data.status_code in [i for i in range(200, 299)]:
                            console.log(
                                f"[turquoise4]> Metadata of [/turquoise4][cyan]SCP-{scp_num}[/cyan][turquoise4] accessed, status code: {scp_data.status_code}, writing to database ...[/turquoise4]"
                            )
                            with open(
                                    f"database/anomalies.list.d/scp_{scp_num}.info", "w"
                                ) as scp_info:
                                scp_info.write(soup.prettify())
                            console.log(
                                f"[green]> Data of [/green][cyan]SCP-{scp_num}[/cyan][green] written successfully to database.[/green]"
                            )
                        else:
                            console.log(
                                f"[red]> Skipping [/red][cyan]SCP-{scp_num}[/cyan][red], connection error.[/red]"
                            )

                end_time = process_time()
                console.log(
                    f"[bold][green][+] Database initiated with total time of:[/green][cyan]{end_time-start_time}[/cyan][/bold]"
                )


database_init()
