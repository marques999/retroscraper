import sys
import json

from pathlib import Path
from itertools import groupby
from operator import itemgetter

from tools import get_roms
from platforms import ROM_EXTENSIONS
from skyscraper import read_database

def filter_entry(entry):

    title, filename = entry
    roms_directory = reversed(Path(filename).parts[:-1])
    suffix = next(roms_directory, False)

    if not suffix or suffix == "#" or (len(suffix) == 1 and suffix.isalpha()):
        return title

    return f"{title} ({next(roms_directory)})"

def print_result(duplicates):

    print(len(duplicates))

    json.dump({
        title: filenames
        for title, filenames in duplicates.items()
        if len(filenames) > 1
    }, sys.stdout, indent=2)

def print_duplicates(platform):

    roms_directory = Path.home() / "RetroPie" / "roms" / platform
    cache_directory = Path.home() / ".skyscraper" / "cache" / platform
    roms = get_roms(roms_directory, ROM_EXTENSIONS.get(platform))
    gamedb = read_database(cache_directory)

    entries = sorted((
        (game["title"].upper(), roms[checksum])
        for (checksum, game) in gamedb.items()), key=itemgetter(0)
    )

    print_result(dict(
        (group, list(map(itemgetter(1), items)))
        for group, items in groupby(entries, key=itemgetter(0))
    ))

def print_duplicates_region(platform):

    roms_directory = Path.home() / "RetroPie" / "roms" / platform
    cache_directory = Path.home() / ".skyscraper" / "cache" / platform
    roms = get_roms(roms_directory, ROM_EXTENSIONS.get(platform))
    gamedb = read_database(cache_directory)

    entries = sorted(
        ((game["title"].upper(), str(Path(roms[checksum]).relative_to(roms_directory)))
         for (checksum, game) in gamedb.items()),
        key=filter_entry
    )

    print_result(dict(
        (group, list(map(itemgetter(1), items)))
        for group, items in groupby(entries, key=filter_entry)
    ))
