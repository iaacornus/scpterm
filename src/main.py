import sys
import os

from utils.database_init import database_init
from utils.md_init import md_init


def main(scp_num):
    sys.path.append("..")
    if not os.path.isfile("database/fetch"):
        database_init()

    md_init(scp_num)
