from argparse import ArgumentParser

from yennie import check_assets, check_yennie
from organize import organize_directories, organize_rename
from duplicates import print_duplicates, print_duplicates_region

HANDLERS = {
    "assets": check_assets,
    "yennie": check_yennie,
    "rename": organize_rename,
    "duplicates": print_duplicates,
    "organize": organize_directories,
    "duplicates-region": print_duplicates_region
}

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("command", choices=HANDLERS.keys())
    parser.add_argument("platform")
    arguments = parser.parse_args()
    HANDLERS[arguments.command](arguments.platform)
