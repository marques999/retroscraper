import os
import sys
import json

from pathlib import Path
from deepmerge import merge
from itertools import groupby
from platforms import ROM_EXTENSIONS
from tools import digest_file, get_files, get_roms

def get_checksums(directory):

    return set(
        os.path.basename(os.path.splitext(filename)[0])
        for filename in get_files(directory, [".png"])
    )

def get_duplicates(media_directory, roms_lookup):

    duplicates = {}
    filenames = get_files(media_directory, [".png"])

    for group, grouper in groupby(sorted(filenames, key=digest_file), key=digest_file):

        checksums = map(lambda filename: os.path.splitext(os.path.basename(filename))[0], grouper)
        roms = list(map(roms_lookup.get, filter(roms_lookup.get, checksums)))

        if len(roms) > 1:
            duplicates[group] = roms

    return duplicates

def check_yennie(platform):

    missing = {}
    roms_directory = Path.home() / "RetroPie" / "roms" / platform
    media_directory = Path.home() / ".skyscraper" / "cache" / platform
    roms = get_roms(roms_directory, ROM_EXTENSIONS.get(platform))

    for media in ["screenshots", "covers", "wheels"]:
        directory = media_directory / media / "screenscraper"
        missing = merge(missing, get_duplicates(directory, roms))

    json.dump(missing, sys.stdout, indent=2)

def check_assets(platform):

    media_directory = Path.home() / ".skyscraper" / "cache" / platform
    covers = get_checksums(media_directory / "covers" / "screenscraper")
    wheels = get_checksums(media_directory / "wheels" / "screenscraper")
    screenshots = get_checksums(media_directory / "screenshots" / "screenscraper")

    available_union = covers | wheels | screenshots
    available_intersection = covers & wheels & screenshots
    missing = available_union.symmetric_difference(available_intersection)

    roms = get_roms(
        Path.home() / "RetroPie" / "roms" / platform,
        ROM_EXTENSIONS.get(platform)
    )

    missing = list(map(roms.get, filter(roms.get, missing)))
    json.dump(missing, sys.stdout, indent=2)
