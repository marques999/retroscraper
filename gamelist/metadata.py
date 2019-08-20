import os
import colorama

from operator import itemgetter
from pathlib import Path, PurePath
from argparse import ArgumentParser

from tools import get_roms
from pegasus import PegasusMetadata
from platforms import ROM_EXTENSIONS
from skyscraper import SkyscraperMetadata

EXPORTERS = {
    "attractmode": None,
    "emulationstation": None,
    "pegasus": PegasusMetadata
}

class GamelistContext:

    __slots__ = ("platform", "roms_directory", "media_directory")

    def __init__(self, platform, roms_directory, media_directory):
        self.platform = platform
        self.roms_directory = roms_directory
        self.media_directory = media_directory


def filter_games(context, gamedb):

    gamedb_missing = []
    gamedb_available = []
    roms = context["roms"]

    for (checksum, game) in gamedb.items():

        if checksum not in roms:
            continue

        missing_medias = get_missing_medias(context, game)

        if missing_medias:
            gamedb_missing.append((roms[checksum], missing_medias))
        else:
            gamedb_available.append((roms[checksum], checksum, game))

    return sorted(gamedb_available, key=itemgetter(0)), gamedb_missing

def get_missing_medias(context, game):

    return [
        media
        for media in context["medias"]
        if media not in game or not os.path.exists(context["media_directory"] / game[media])
    ]

def get_required_medias(context):

    return set(
        media[len("no_"):-1]
        for media in ["no_covers", "no_marquees", "no_screenshots", "no_wheels"]
        if media not in context or context[media] == False
    )

if __name__ == "__main__":

    colorama.init(autoreset=True)
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--platform", required=True, choices=ROM_EXTENSIONS.keys())
    parser.add_argument("--frontend", default="pegasus", choices=EXPORTERS.keys())
    parser.add_argument("--roms_directory")
    parser.add_argument("--media_directory")
    parser.add_argument("--output", required=False)
    parser.add_argument("--no-covers", action="store_true")
    parser.add_argument("--no-marquees", action="store_true")
    parser.add_argument("--no-screenshots", action="store_true")
    parser.add_argument("--no-wheels", action="store_true")
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()

    if arguments.media_directory:
        media_directory = PurePath(arguments.media_directory)
    else:
        media_directory = Path.home() / ".skyscraper" / "cache" / arguments.platform

    if arguments.roms_directory:
        roms_directory = PurePath(arguments.roms_directory)
    else:
        roms_directory = Path.home() / "RetroPie" / "roms" / arguments.platform

    if arguments.output:
        output_directory = Path(arguments.output) / arguments.platform
    else:
        output_directory = Path.cwd()

    context = {
        "platform": arguments.platform,
        "roms_directory": roms_directory,
        "media_directory": media_directory,
        "output_directory": output_directory,
        "medias": get_required_medias(vars(arguments)),
        "roms": get_roms(roms_directory, ROM_EXTENSIONS[arguments.platform])
    }

    gamedb = SkyscraperMetadata().read(media_directory)
    gamedb_available, gamedb_missing = filter_games(context, gamedb)
    exporter = EXPORTERS[arguments.frontend](context)

    for (filename, medias) in gamedb_missing:

        print("%s[  SKIP  ]%s %s %s(%s) " % (
            colorama.Fore.RED,
            colorama.Fore.RESET,
            filename,
            colorama.Fore.RED,
            ", ".join(medias)
        ))

    if arguments.debug:

        from organize import organize_roms

        for (source, destination) in organize_roms(context, gamedb_available):

            print("%s[ COPY ]%s %s -> %s%s" % (
                colorama.Fore.GREEN,
                colorama.Fore.RESET,
                source,
                colorama.Fore.CYAN,
                destination
            ))

        exporter.debug(gamedb_available)

    else:

        exporter.write(gamedb_available, output_directory)
