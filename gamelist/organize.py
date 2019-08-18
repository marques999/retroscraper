import os

from pathlib import Path
from skyscraper import read_database
from platforms import ROM_EXTENSIONS
from tools import digest_file, get_roms

def organize_directories(platform):

    roms_directory = Path.home() / "RetroPie" / "roms" / platform
    cache_directory = Path.home() / ".skyscraper" / "cache" / platform
    roms = get_roms(roms_directory, ROM_EXTENSIONS.get(platform))
    gamedb = read_database(cache_directory)

    entries = [
        (game["title"].upper(), roms[checksum])
        for (checksum, game) in gamedb.items()
    ]

    for title, filename in entries:

        rom_directory = Path(os.path.dirname(filename))
        rom_suffix = rom_directory.parts[-1]

        if title[0].isalpha():
            organized_suffix = title[0].upper()
        else:
            organized_suffix = "#"

        has_valid_suffix = rom_suffix == "#" or (len(rom_suffix) == 1 and rom_suffix.isalpha())

        if has_valid_suffix and rom_suffix.upper() == organized_suffix:
            continue

        if has_valid_suffix:
            organized_directory = rom_directory.joinpath("..", organized_suffix).resolve()
        else:
            organized_directory = rom_directory.joinpath(organized_suffix)

        if not os.path.exists(organized_directory):
            os.mkdir(organized_directory)

        os.rename(filename, organized_directory.joinpath(os.path.basename(filename)))

def organize_rename(roms_directory):

    for root, _, filenames in os.walk(roms_directory, topdown=False):

        if "media" in Path(root).relative_to(roms_directory).parts:
            continue

        for filename in filenames:

            source_filename = os.path.join(root, filename)

            if filename == "gamelist.xml" or os.path.isdir(source_filename):
                continue

            checksum = digest_file(source_filename)
            extension = os.path.splitext(filename)[-1]
            target_filename = Path(root).joinpath(checksum).with_suffix(extension)

            if os.path.exists(target_filename):
                continue

            os.rename(source_filename, target_filename)
            print(source_filename, "->", target_filename)
