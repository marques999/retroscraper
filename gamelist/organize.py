from os import path
from pathlib import PurePath

from tools import get_roms
from inflection import singularize
from skyscraper import SkyscraperMetadata

def get_suffix(title):

    if title[0].isalpha():
        return title[0].upper()
    else:
        return "#"

def organize_directories(context):

    filenames = []
    gamedb = SkyscraperMetadata().read(context["media_directory"])
    roms = get_roms(context["roms_directory"], context["extensions"])

    entries = (
        (game["title"].upper(), roms[checksum])
        for (checksum, game) in gamedb.items()
        if checksum in roms
    )

    for title, filename in entries:

        rom_directory = PurePath(path.dirname(filename))
        rom_suffix = rom_directory.parts[-1]
        organized_suffix = get_suffix(title)
        has_valid_suffix = rom_suffix == "#" or (
            len(rom_suffix) == 1 and rom_suffix.isalpha())

        if has_valid_suffix and rom_suffix.upper() == organized_suffix:
            continue

        if has_valid_suffix:
            organized_directory = (rom_directory / ".." / organized_suffix).resolve()
        else:
            organized_directory = rom_directory / organized_suffix

        filenames.append((
            filename,
            organized_directory / path.basename(filename)
        ))

    return filenames

def rename_rom(context, filename, checksum):

    return context["output_directory"] / PurePath(filename) \
        .relative_to(context["roms_directory"]) \
        .with_name(checksum) \
        .with_suffix(path.splitext(filename)[-1])

def organize_rename(context):

    roms = get_roms(context["roms_directory"], context["extensions"])
    gamedb = SkyscraperMetadata().read(context["media_directory"])

    return (
        (filename, rename_rom(context, filename, checksum))
        for (checksum, filename) in roms.items()
        if checksum in gamedb
    )

def organize_roms(context, gamedb):

    filenames = []

    for (source, checksum, game) in gamedb:

        destination = PurePath(context["output_directory"]) \
            .joinpath(get_suffix(game["title"])) \
            .joinpath(checksum) \
            .with_suffix(path.splitext(source)[-1])

        paths = {
            "rom": (source, destination)
        }

        for media in context["medias"]:

            media_directory = game.get(singularize(media))

            if media_directory:

                paths[media] = (
                    context["media_directory"] / media_directory,
                    context["output_directory"] / media / path.basename(media_directory)
                )

        filenames.append(paths)

    return filenames
