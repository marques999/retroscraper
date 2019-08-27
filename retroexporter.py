#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import colorama

from operator import itemgetter
from pathlib import Path, PurePath
from argparse import ArgumentParser

from shared.platforms import PLATFORMS

from exporter.tools import get_roms
from exporter.organize import organize_roms
from exporter.pegasus import PegasusExporter
from exporter.emulationstation import EsExporter
from exporter.skyscraper import SkyscraperImporter

EXPORTERS = {
    "pegasus": PegasusExporter,
    "emulationstation": EsExporter
}

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
        #else:
        gamedb_available.append((roms[checksum], game))

    return (
        sorted(gamedb_available, key=itemgetter(0)),
        sorted(gamedb_missing, key=itemgetter(0))
    )

def get_missing_medias(context, game):

    return [
        media
        for media in context["medias"]
        if media not in game or not os.path.exists(context["media_directory"] / game[media])
    ]

def get_required_medias(context):

    return set(
        media
        for media in ["covers", "marquees", "screenshots", "wheels"]
        if "no_" + media not in context or context["no_" + media] == False
    )

if __name__ == "__main__":

    colorama.init(autoreset=True)
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--platform", required=True, choices=PLATFORMS.keys())
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
    extensions = PLATFORMS[arguments.platform].get("extensions")

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
        "roms": get_roms(roms_directory, extensions),
        "medias": get_required_medias(vars(arguments))
    }

    gamedb = SkyscraperImporter(context).read(media_directory)
    gamedb_available, gamedb_missing = filter_games(context, gamedb)
    exporter = EXPORTERS[arguments.frontend](context)

    for (filename, medias) in gamedb_missing:

        print("%s[ SKIP ]%s %s %s(%s) " % (
            colorama.Fore.RED,
            colorama.Fore.RESET,
            filename,
            colorama.Fore.RED,
            ", ".join(medias)
        ))

    if arguments.debug:

        for entry in organize_roms(context, gamedb_available):

            source, destination = entry["rom"]

            print("%s[ COPY ]%s %s -> %s%s" % (
                colorama.Fore.GREEN,
                colorama.Fore.RESET,
                source,
                colorama.Fore.CYAN,
                destination
            ))

        print(exporter.debug(gamedb_available))

    else:

        exporter.write(gamedb_available, output_directory)
