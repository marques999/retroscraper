# -*- coding: utf-8 -*-

from os import getcwd
from pathlib import PurePath
from itertools import groupby
from xml.etree import ElementTree

from shared import handlers
from shared.platforms import PLATFORMS
from shared.gdf import GdfFields, GdfRegion
from shared.tools import export, merge_dictionaries, parse_datetime

def export_platform(context, value):

    return next((
        id for id, platform in PLATFORMS.items()
        if platform["name"].lower() == value.lower()
    ), value)

def chain_wrap(key, handler):
    return lambda context, value: {key: handler(context, value)}

def export_rating(context, value):
    return int(round(float(value) * 100))

def export_media(context, value):
    return context.gdfpath.joinpath(value)

SKYSCRAPER_PARSER = {
    GdfFields.TITLE: ("title", chain_wrap(GdfRegion.WORLD, handlers.string)),
    GdfFields.PLATFORM: ("platform", export_platform),
    GdfFields.DESCRIPTION: ("description", chain_wrap("en", handlers.string)),
    GdfFields.COVER: ("cover", chain_wrap(GdfRegion.WORLD, export_media)),
    GdfFields.SCREENSHOT: ("screnshot",  chain_wrap(GdfRegion.WORLD, export_media)),
    GdfFields.WHEEL: ("wheel", chain_wrap(GdfRegion.WORLD, export_media)),
    GdfFields.GENRE: ("tags", handlers.string),
    GdfFields.RATING: ("rating", export_rating),
    GdfFields.AGES: ("ages", handlers.string),
    GdfFields.RELEASE: ("releasedate", chain_wrap(GdfRegion.WORLD, parse_datetime)),
    GdfFields.PLAYERS: ("players", handlers.string),
    GdfFields.DEVELOPER: ("developer", handlers.string),
    GdfFields.PUBLISHER: ("publisher", handlers.string)
}

class SkyscraperProvider(object):

    ID = "skyscraper"
    URL = PurePath(getcwd()) / "cache"

    DEFAULTS = {
        "id": 0,
        "parent": 0,
        "ignore": False
    }

    def __init__(self, platform, directory=None):

        self.platform = platform
        self.directory = directory or self.URL
        self.gdfpath = (self.directory / platform)
        self.database = self.__read_skyscraper()

    def __read_skyscraper(self):

        gamedb = {}
        xml_filename = (self.gdfpath / "db.xml")
        root = ElementTree.parse(xml_filename).getroot()
        entries = sorted(root, key=lambda entry: entry.attrib["sha1"])
        groups = groupby(entries, key=lambda entry: entry.attrib["sha1"])

        for (checksum, attributes) in groups:

            properties = export(SKYSCRAPER_PARSER, self, {
                entry.attrib["type"]: entry.text
                for entry in attributes
            })

            properties["checksum"] = checksum
            gamedb[checksum] = merge_dictionaries(self.DEFAULTS, properties)

        return gamedb
