# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import groupby
from operator import itemgetter

from exporter.tools import get_roms
from exporter.skyscraper import SkyscraperImporter

def filter_entry(entry):

    title, filename = entry
    roms_directory = reversed(Path(filename).parts[:-1])
    suffix = next(roms_directory, False)

    if not suffix or suffix == "#" or (len(suffix) == 1 and suffix.isalpha()):
        return title

    return f"{title} ({next(roms_directory)})"

def duplicates_recursive(context):

    gamedb = SkyscraperImporter(context).read(context["media_directory"])
    roms = get_roms(context["roms_directory"], context["extensions"])

    entries = sorted((
        (game["title"].upper(), roms[checksum])
        for (checksum, game) in gamedb.items()), key=itemgetter(0)
    )

    return dict(
        (group, list(map(itemgetter(1), grouper)))
        for group, grouper in groupby(entries, key=itemgetter(0))
    )

def duplicates_region(context):

    roms_directory = context["roms_directory"]
    roms = get_roms(roms_directory, context["extensions"])
    gamedb = SkyscraperImporter(context).read(context["media_directory"])

    entries = sorted(
        ((game["title"].upper(), str(Path(roms[checksum]).relative_to(roms_directory)))
         for (checksum, game) in gamedb.items()),
        key=filter_entry
    )

    return dict(
        (group, list(map(itemgetter(1), items)))
        for group, items in groupby(entries, key=filter_entry)
    )
