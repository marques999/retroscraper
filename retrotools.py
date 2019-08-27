#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

from pathlib import Path
from argparse import ArgumentParser
from shared.platforms import PLATFORMS

from exporter.yennie import check_assets, check_yennie
from exporter.organize import organize_directories, organize_rename
from exporter.duplicates import duplicates_recursive, duplicates_region

def print_result(duplicates):

    print(len(duplicates))

    json.dump({
        title: filenames
        for title, filenames in duplicates.items()
        if len(filenames) > 1
    }, sys.stdout, indent=2)

def get_context(platform):

    return {
        "platform": platform,
        "medias": {"covers", "screenshots", "wheels"},
        "extensions": PLATFORMS[platform].get("extensions"),
        "output_directory": Path("G:\\RetroPie") / platform,
        "roms_directory": Path.home() / "RetroPie" / "roms" / platform,
        "media_directory": Path.home() / ".skyscraper" / "cache" / platform
    }

def duplicates_region_cli(platform, debug):

    print_result(duplicates_region(get_context(platform)))

def duplicates_recursive_cli(platform, debug):

    print_result(duplicates_recursive(get_context(platform)))

def check_assets_cli(platform, debug):

    json.dump(check_assets(get_context(platform)), sys.stdout, indent=2)

def check_yennie_cli(platform, debug):

    json.dump(check_yennie(get_context(platform)), sys.stdout, indent=2)

def organize_directories_cli(platform, debug):

    context = get_context(platform)

    for (filename, destination_directory) in organize_directories(context):

        if not os.path.exists(destination_directory):
            os.mkdir(destination_directory)

        destination = destination_directory.joinpath(os.path.basename(filename))

        if debug:
            print(filename, "->", destination)
        else:
            os.rename(filename, destination)

def organize_rename_cli(platform, debug):

    for (source, destination) in organize_rename(get_context(platform)):

        if os.path.exists(destination):
            continue

        if debug:
            print(source, "->", destination)
        else:
            os.rename(source, destination)

if __name__ == "__main__":

    handlers = {
        "assets": check_assets_cli,
        "yennie": check_yennie_cli,
        "rename": organize_rename_cli,
        "organize": organize_directories_cli,
        "duplicates-region": duplicates_region_cli,
        "duplicates-recursive": duplicates_recursive_cli
    }

    parser = ArgumentParser()
    parser.add_argument("command", choices=handlers.keys())
    parser.add_argument("platform", choices=PLATFORMS.keys())
    parser.add_argument("--debug", action="store_true")
    arguments = parser.parse_args()
    handlers[arguments.command](arguments.platform, arguments.debug)
