import os

from xml.dom import minidom
from itertools import groupby
from xml.etree import ElementTree
from pathlib import Path, PurePath
from argparse import ArgumentParser

from pegasus import PegasusExporter
from platforms import ROM_EXTENSIONS
from skyscraper import read_database
from tools import digest_file, digest_gzip, digest_zip, get_roms

EXPORTERS = {
    "emulationstation": None,
    "pegasus": PegasusExporter
}

def filter_games(context, gamedb):

    gamedb_missing = []
    gamedb_available = []
    roms = get_roms(context.roms_directory, ROM_EXTENSIONS[context.platform])

    for (checksum, game) in gamedb.items():

        if checksum not in roms:
            continue

        medias_missing = [
            media
            for media in ["cover", "screenshot", "wheel"]
            if media not in game or not os.path.exists(context.media_directory / game[media])
        ]

        if medias_missing:
            gamedb_missing.append((roms[checksum], medias_missing))
        else:
            gamedb_available.append({**game, "path": roms[checksum]})

    gamedb_available.sort(key=lambda entry: entry["title"])

    return gamedb_available, gamedb_missing

class GamelistContext:

    __slots__ = ("platform", "roms_directory", "media_directory")

    def __init__(self, platform, roms_directory, media_directory):
        self.platform = platform
        self.roms_directory = roms_directory
        self.media_directory = media_directory

if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--frontend", default="pegasus", choices=EXPORTERS.keys())
    parser.add_argument("--output", required=False)
    arguments = parser.parse_args()

    context = GamelistContext(
        platform=arguments.platform,
        roms_directory=Path.home() /  "RetroPie" / "roms" / arguments.platform,
        media_directory=Path.home() / ".skyscraper" / "cache" / arguments.platform
    )

    exporter = EXPORTERS[arguments.frontend](context)
    gamedb_available, gamedb_missing = filter_games(
        context, read_database(context.media_directory))

    if arguments.debug:
        exporter.generate_metadata(gamedb_available)
    else:
        output_directory = os.path.join(os.path.abspath(arguments.output), arguments.platform)
        exporter.write_metadata(gamedb_available, output_directory)
