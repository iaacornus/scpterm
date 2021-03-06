import argparse

from rich.console import Console

from main import main
from utils.database_init import database_init
from utils.scp_utils import Utils

def program_options():
    console = Console()
    utils = Utils()

    description = """\
        scpterm, a view classified information of SCP Foundation's anomalies in your terminal.
    """
    parser = argparse.ArgumentParser(
        prog="scp",
        usage="scp [COMMAND] [OPTIONS] [INPUT]",
        description=description
    )

    parser.add_argument(
        "-init",
        "--initiate",
        help="Initiate the database.",
        action="store_true"
    )
    parser.add_argument(
        "-r",
        "--re",
        help="Do again the previous task",
        action="store_true"
    )
    # view the information of anomaly
    parser.add_argument(
        "-d",
        "--decode",
        help="View the information of anomaly.",
        action="store"
    )
    parser.add_argument(
        "-I",
        "--image",
        help="Display the image of the anomaly.",
        action="store"
    )
    parser.add_argument(
        "-l",
        "--list",
        help="List all available anomaly.",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Show the version number of the software as well as other information.",
        action="store_true"
    )

    args = parser.parse_args()

    try:
        if args.initiate:
            database_init(args.re)
        elif args.decode:
            main(args.decode)
        elif args.list:
            utils.scp_list()
        elif args.image:
            utils.view_img(args.image)
        elif args.version:
            with open("software.info", "r", encoding="utf-8") as info:
                software_info = info.readlines()

            for lines in software_info:
                print(lines.replace("\n", ""))

            if "y" in console.input("[bold][:] Read license? [/bold]"):
                with open("LICENSE", "r", encoding="utf-8") as _license_:
                    software_license = _license_.readlines()

                for lines in software_license:
                    print(lines.replace("\n", ""))
        else:
            console.log(
                "[bold red][-] Options not found.[/bold red]"
            )
            raise SystemExit
    except ConnectionError: # add other exceptions later
        console.log(
            "[bold red][-] Connection error.[/bold red]"
        )
        raise SystemExit
    except KeyboardInterrupt:
        console.log(
            "[bold red][-] Keyboard interrupt.[/bold red]"
        )
        raise SystemExit
    except SystemError:
        console.log(
            "[bold red][-] System error.[/bold red]"
        )
        raise SystemExit


if __name__ == "__main__":
    program_options()
