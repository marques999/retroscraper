from os import path
from functools import reduce
from itertools import groupby
from operator import itemgetter

from deepmerge import merge
from tools import digest_file, get_files, get_roms

def remove_extension(filename):

    return path.basename(path.splitext(filename)[0])

def get_checksums(directory):

    return set(map(remove_extension, get_files(directory, [".png"])))

def get_duplicates(media_directory, roms_lookup):

    duplicates = {}

    filenames = sorted((
        (filename, digest_file(filename))
        for filename in get_files(media_directory, [".png"])), key=itemgetter(1)
    )

    for group, grouper in groupby(filenames, key=itemgetter(1)):

        checksums = map(remove_extension, map(itemgetter(0), grouper))
        roms = list(map(roms_lookup.get, filter(roms_lookup.get, checksums)))

        if len(roms) > 1:
            duplicates[group] = roms

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
