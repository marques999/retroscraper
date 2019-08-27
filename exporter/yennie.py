# -*- coding: utf-8 -*-

from os import path
from functools import reduce
from itertools import groupby
from operator import itemgetter

from shared.tools import get_files

from exporter.deepmerge import merge
from exporter.tools import digest_file, get_roms

def remove_extension(filename):

    return path.basename(path.splitext(filename)[0])

def get_checksums(directory):

    return set(map(remove_extension, get_files(directory, [".png"])))

def get_duplicates(media_directory, roms):

    filenames = sorted((
        (filename, digest_file(filename))
        for filename in get_files(media_directory, [".png"])), key=itemgetter(1)
    )

    duplicates = {}

    for group, grouper in groupby(filenames, key=itemgetter(1)):

        checksums = map(remove_extension, map(itemgetter(0), grouper))
        matches = list(map(roms.get, filter(roms.get, checksums)))

        if len(matches) > 1:
            duplicates[group] = matches

    return duplicates

def check_assets(context):

    medias = [
        get_checksums(context["media_directory"] / media / "screenscraper")
        for media in context["medias"]
    ]

    roms = get_roms(context["roms_directory"], context["extensions"])
    missing = set.union(*medias).symmetric_difference(set.intersection(*medias))

    return list(map(roms.get, filter(roms.get, missing)))

def check_yennie(context):

    roms = get_roms(context["roms_directory"], context["extensions"])

    return reduce(lambda result, media: merge(result, get_duplicates(
        context["media_directory"] / media / "screenscraper", roms
    )), context["medias"], {})
