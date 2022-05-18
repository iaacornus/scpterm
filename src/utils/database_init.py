import sys
sys.path.append("..")

from datetime import datetime as time
from os import path

import requests
from random_user_agent.user_agent import UserAgent
from bs4 import BeautifulSoup as bs
from rich.console import Console

def database_init():
    console = Console()
    user_agent = UserAgent()
    link = "https://the-scp.foundation/object"

    if path.isfile("database/fetch"):
        with open("database/fetch", "r") as data:
            data_info = data.readlines()

        console.log(
            f"[bold][+] Database already exists (last fetch:[cyan]{data_info[1]}[/cyan]), skipping.[/bold]"
        )
    else:
        try:
            with console.status(
                "[bold turquoise4][=] Checking access to database ...[/bold turquoise4]",
                spinner="bouncingBar"
            ):
                header = {"User-Agent": user_agent.get_random_user_agent()}
                #response = requests.get(link, headers=header)
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
                        scp_link = f"{link}/{scp_num}"
                        anomalies.write(f"SCP-{scp_num}: {scp_link}\n")

                        console.log(
                            f"[turquoise4]> Fetching [turquoise4][bold wheat4]SCP-{scp_num}[/bold wheat4]"
                        )

                    # fetch the html from the page


database_init()
