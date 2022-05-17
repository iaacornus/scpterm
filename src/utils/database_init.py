from time import sleep
from random import uniform

import requests
from random_user_agent.user_agent import UserAgent
from bs4 import BeautifulSoup as bs
from rich.console import Console

def database_init():
    console = Console()
    user_agent = UserAgent()
    link = "https://the-scp.foundation/object/scp-002"

    try:
        with console.status(
            "[bold turquoise4][+] Checking access to database ...[/bold turquoise4]",
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
            "[bold bright_red][=] Some of the anomalies would not be fetched due to classified reason.[/bold bright_red]\n> Press any key to continue."
        )
        input()

        with console.status(
            "[bold turquoise4][+] Fetching anomalies information ...[/bold turquoise4]",
            spinner="bouncingBar"
        ):
            for i in range(1, 1000):
                if len(f"{i}") == 1:
                    scp_num = f"00{i}"
                elif len(f"{i}") == 2:
                    scp_num = f"0{i}"
                elif len(f"{i}") == 1:
                    scp_num = f"{i}"
                scp_link = f"{link}/{scp_num}"
                console.log(
                    f"[turquoise4]> Fetching [turquoise4][bold wheat4]SCP-{scp_num}[/bold wheat4]"
                )

