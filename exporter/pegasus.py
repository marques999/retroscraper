# -*- coding: utf-8 -*-

from re import sub
from os import path
from datetime import datetime
from textwrap import TextWrapper, dedent

from shared import handlers
from shared.tools import export
from shared.gdf import GdfFields

from exporter.tools import export_media

class PegasusFields(object):

    GAME = "game"
    FILE = "file"
    DEVELOPER = "developer"
    PUBLISHER = "publisher"
    GENRE = "genre"
    DESCRIPTION = "description"
    RELEASE = "release"
    PLAYERS = "players"
    RATING = "rating"
    ASSETS_VIDEO = "assets.video"
    ASSETS_WHEEL = "assets.wheel"
    ASSETS_MARQUEE = "assets.marquee"
    ASSETS_BOXFRONT = "assets.boxfront"
    ASSETS_SCREENSHOT = "assets.screenshots"

def export_players(context, value):
    return value[value.rfind("-") + 1:]

def export_rating(context, value):
    return "{0:.0%}".format(float(value))

def export_rom(context, value):
    return str(context["roms_directory"] / value).replace("\\", "/")

def export_media2(media):
    return lambda context, value: str(export_media(context, media, value)[1])

def export_description(context, value):

        newlines = value.replace("\n", "\\n")
        wrapped = TextWrapper(width=80).wrap(dedent(newlines))

        for (index, line) in enumerate(wrapped):

            result = sub(" +", " ", line)

            if line.startswith("\\n\\n"):
                wrapped[index] = result.replace(
                    "\\n\\n", ".\n  ").replace("\\n", "\\n\n  ")
            else:
                wrapped[index] = result.replace(
                    "\\n\\n", "\n  .\n  ").replace("\\n", "\\n\n  ")

        return "\n  " + "\n  ".join(wrapped)

PEGASUS_EXPORTER = {
    PegasusFields.GAME: (GdfFields.TITLE, handlers.string),
    PegasusFields.FILE: (GdfFields.PATH, export_rom),
    PegasusFields.DEVELOPER: (GdfFields.DEVELOPER, handlers.string),
    PegasusFields.PUBLISHER: (GdfFields.PUBLISHER, handlers.string),
    PegasusFields.GENRE: (GdfFields.GENRE, handlers.string),
    PegasusFields.DESCRIPTION: (GdfFields.DESCRIPTION, export_description),
    PegasusFields.RELEASE: (GdfFields.RELEASE, handlers.timestamp("%Y-%m-%d")),
    PegasusFields.PLAYERS: (GdfFields.PLAYERS, export_players),
    PegasusFields.RATING: (GdfFields.RATING, export_rating),
    PegasusFields.ASSETS_BOXFRONT: (GdfFields.COVER, export_media2("covers")),
    PegasusFields.ASSETS_SCREENSHOT: (GdfFields.SCREENSHOT, export_media2("screenshots")),
    PegasusFields.ASSETS_WHEEL: (GdfFields.WHEEL, export_media2("wheels")),
    PegasusFields.ASSETS_MARQUEE: (GdfFields.MARQUEE, export_media2("marquees")),
    PegasusFields.ASSETS_VIDEO: (GdfFields.VIDEO, export_media2("videos"))
}

class PegasusExporter(object):

    def __init__(self, context):

        self.context = context

    def debug(self, entries):

        return self.__generate_metadata(entries)

    def write(self, entries, path):

        filename = path / "metadata.pegasus.txt"

        with open(filename, mode="w", encoding="utf-8") as stream:
            stream.write(self.__generate_metadata(entries))

    def __generate_metadata(self, entries):

        return "\n\n\n".join(map(self.__generate_entry, entries))

    def __generate_entry(self, entry):

        return "\n".join(
            "%s: %s" % (key, value)
            for (key, value) in export(self.PEGASUS_EXPORTER, self.context, entry[1])
            if value and len(value)
        )

# metadata_filename = "D:\\Atari 7800 [US]\\metadata.pegasus.txt"

# with open(metadata_filename, mode="r", encoding="utf-8") as stream:
#     contents = stream.read().split("\n\n\n")
#     entries = iter(contents[0].split("\n"))
#     mapping = {}
#     while entries:
#         key, _, value = next(entries, "").partition(": ")
#         if key == "description":
#             print(list(takewhile(lambda x: x.startswith("  "), entries)))
#         else:
#             mapping[key] = value

#     print(mapping)
