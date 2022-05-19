import os
import sys
from time import process_time, sleep
from random import uniform

import requests
import cv2 as cv
from bs4 import BeautifulSoup as bs
from random_user_agent.user_agent import UserAgent
from rich.console import Console
from rich.markdown import Markdown


class Utils:
    sys.path.append("..")
    console = Console()

    def __init__(self):
        pass

    def check_status(self, link, user_agent):
        with self.console.status(
                "[bold turquoise4][=] Checking access to database ...[/bold turquoise4]",
                spinner="bouncingBar"
            ):
            response = requests.get(link, headers={"User-Agent": user_agent})

            if response.status_code not in list(range(200, 299)):
                raise ConnectionError

    def scp_search(self, scp_num):
        user_agent = UserAgent()
        start_time = process_time()
        link = f"https://the-scp.foundation/object/scp-{scp_num}"

        try:
            self.check_status(link, user_agent.get_random_user_agent())
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

    def fetch_soup(self, scp_num):
        if os.path.isfile(f"database/anomalies.list.d/scp_{scp_num}.info"):
            with open(
                f"database/anomalies.list.d/scp_{scp_num}.info", "r", encoding="utf-8"
            ) as scp_info:
                index = scp_info.read()
                soup = bs(index, "html5lib")

                return True, soup
        else:
            self.console.log(
                f"[bold][red][-] [/red][cyan]SCP-{scp_num}[/cyan][red] does not exist.[/red]"
            )
            return False, None

    def check_img(self, scp_num):
        for type_ in ["jpg", "png"]:
            img_path = f"database/scp_imgs/scp_{scp_num}_img.{type_}"
            if os.path.exists(img_path):
                return True, img_path

        return False, None

    def fetch_img(self, scp_num):
        scp_img_check, scp_img_path = self.check_img(scp_num)

        if scp_img_check:
            return True, scp_img_path
        else:
            (check, soup), trial = self.fetch_soup(scp_num), 0
            while not check:
                self.console.log(
                    f"[red]> Failed attempt, try: {trial}[/red]"
                )
                if trial == 2:
                    self.console.log(
                        "[bold red][-] Too many failed attempts, aborting.[/bold red]"
                    )
                    break
                if "y" in self.console.input(
                        f"[bold][:] Check SCP-{scp_num} in online database? [/bold]"
                    ).lower():
                    self.scp_search(scp_num)
                    check, soup = self.fetch_soup(scp_num)

            with self.console.status(
                "[bold turquoise4][=] Fetching img of the anomaly ...[/bold turquoise4]"
            ):
                if not os.path.exists("database/scp_imgs"):
                    os.mkdir("database/scp_imgs")

                scp_img_metadata = soup.find("img", {"class": "scp-image"})
                scp_img = str(scp_img_metadata).rsplit(" ", maxsplit=1)[-1]
                # scp_img = str(scp_img_metadata).split(" ")[-1][5:-3]


                if scp_img.startswith("https://"):
                    try:
                        img = requests.get(scp_img)
                        img_name = f"scp_{scp_num}_img.{scp_img[-3:]}"

                        with open(f"database/scp_imgs/{img_name}", "wb") as img_data:
                            img_data.write(img.content)
                    except ConnectionError:
                        self.console.log(
                            "[bold red][-] Database is offline, cannot fetch files.[/bold red]"
                        )
                    else:
                        return True, f"database/scp_imgs/{img_name}"

    def view_img(self, scp_num):
        check, img_dir = self.check_img(scp_num)

        while True:
            if check:
                try:
                    img = cv.imread(f"{img_dir}", cv.IMREAD_ANYCOLOR)
                    while True:
                        cv.imshow(f"SCP-{scp_num}", img)
                        if cv.waitKey(1) & 0xFF == ord("q"):
                            break
                    cv.destroyAllWindows()
                except FileNotFoundError:
                    self.console.log(
                        "[bold red][-] The image requested does not exist in database.[/bold red]"
                    )
                else:
                    return True
            else:
                check, img_dir = self.fetch_img(scp_num)
                continue

    def view_md(self, scp_num):
        with self.console.status(
            "[bold turquoise4][=] Opening decoded file ...[/bold turquoise4]",
            spinner="bouncingBar"
        ):
            sleep(uniform(0.1, 5.0))
            with open(f"database/proc.anomalies.d/scp_{scp_num}.md") as scp_data:
                scp_md = Markdown(scp_data.read())

            self.console.print(scp_md)

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
