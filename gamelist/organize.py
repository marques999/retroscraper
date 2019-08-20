from os import path
from pathlib import Path

from tools import get_roms
from platforms import ROM_EXTENSIONS
from skyscraper import SkyscraperMetadata


def get_suffix(title):

    if title[0].isalpha():
        return title[0].upper()
    else:
        return "#"


def organize_directories(context):

    filenames = []
    roms = context["roms"]
    gamedb = SkyscraperMetadata().read(context["media_directory"])

    entries = (
        (game["title"].upper(), roms[checksum])
        for (checksum, game) in gamedb.items()
        if checksum in roms
    )

    for title, filename in entries:

        rom_directory = Path(path.dirname(filename))
        rom_suffix = rom_directory.parts[-1]
        organized_suffix = get_suffix(title)
        has_valid_suffix = rom_suffix == "#" or (
            len(rom_suffix) == 1 and rom_suffix.isalpha())

        if has_valid_suffix and rom_suffix.upper() == organized_suffix:
            continue

        if has_valid_suffix:
            organized_directory = rom_directory.joinpath(
                "..", organized_suffix).resolve()
        else:
            organized_directory = rom_directory.joinpath(organized_suffix)

        filenames.append((
            filename,
            organized_directory.joinpath(path.basename(filename))
        ))

    return filenames


def organize_rename(context):

    destination = context["output_directory"]
    gamedb = SkyscraperMetadata().read(context["media_directory"])

    return (
        (filename, Path(destination.joinpath(
            checksum).with_suffix(path.splitext(filename)[-1])))
        for (checksum, filename) in context["roms"].items()
        if checksum in gamedb
    )

def organize_roms(context, gamedb):

    filenames = []

    for (source, checksum, game) in gamedb:

        filenames.append((source, Path(context["output_directory"])
                          .joinpath(get_suffix(game["title"]))
                          .joinpath(checksum)
                          .with_suffix(path.splitext(source)[-1])))

        for media in context["medias"]:

            filenames.append((
                Path(context["media_directory"]) / game[media],
                Path(context["output_directory"]) / (media + "s") / path.basename(game[media])))

    return filenames
