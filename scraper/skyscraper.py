# -*- coding: utf-8 -*-

from os import getcwd
from pathlib import Path
from itertools import groupby
from xml.etree import ElementTree

from scraper.thread import ScraperResponse

from shared import handlers
from shared.platforms import PLATFORMS
from shared.gdf import GdfFields, GdfLanguages, GdfRegions
from shared.tools import export, merge_dictionaries, parse_datetime

def export_rating(context, value):
    return int(round(float(value) * 100))

def export_media(context, value):
    return context.gdfpath.joinpath(value)

def chain_wrap(key, handler):
    return lambda context, value: {key: handler(context, value)}

def export_genres(context, values):
    return list(map(export_genre, enumerate(values.split(", "))))

def export_platform(context, value):

    return next((
        platform_id for platform_id, platform in PLATFORMS.items()
        if platform["name"].lower() == value.lower()
    ), context.platform)

def export_genre(arguments):

    return {
        GdfFields.PARENT: 0,
        GdfFields.ID: arguments[0],
        GdfFields.PRIMARY: arguments[0] == 0,
        GdfFields.DESCRIPTION: {
            GdfLanguages.ENGLISH: arguments[1]
        }
    }

SKYSCRAPER_DEFAULTS = {
    GdfFields.ID: 0,
    GdfFields.PARENT: 0,
    GdfFields.IGNORE: False
}

SKYSCRAPER_PARSER = {
    GdfFields.TITLE: ("title", chain_wrap(GdfRegions.WORLD, handlers.string)),
    GdfFields.PLATFORM: ("platform", export_platform),
    GdfFields.DESCRIPTION: ("description", chain_wrap(GdfLanguages.ENGLISH, handlers.string)),
    GdfFields.COVER: ("cover", chain_wrap(GdfRegions.WORLD, export_media)),
    GdfFields.SCREENSHOT: ("screnshot",  chain_wrap(GdfRegions.WORLD, export_media)),
    GdfFields.WHEEL: ("wheel", chain_wrap(GdfRegions.WORLD, export_media)),
    GdfFields.MARQUEE: ("marquee", chain_wrap(GdfRegions.WORLD, export_media)),
    GdfFields.GENRE: ("tags", export_genres),
    GdfFields.RATING: ("rating", export_rating),
    GdfFields.AGES: ("ages", handlers.string),
    GdfFields.RELEASE: ("releasedate", chain_wrap(GdfRegions.WORLD, parse_datetime)),
    GdfFields.PLAYERS: ("players", handlers.string),
    GdfFields.DEVELOPER: ("developer", handlers.string),
    GdfFields.PUBLISHER: ("publisher", handlers.string)
}

class SkyscraperProvider(object):

    ID = "skyscraper"
    URL = Path.home() / ".skyscraper" / "cache"

    def __init__(self, platform, directory=None):

        self.database = {}
        self.platform = platform
        self.gdfpath = directory or (self.URL / platform)

        root = ElementTree.parse(self.gdfpath / "db.xml").getroot()
        entries = sorted(root, key=lambda entry: entry.attrib["sha1"])
        groups = groupby(entries, key=lambda entry: entry.attrib["sha1"])

        for (checksum, attributes) in groups:

            properties = export(SKYSCRAPER_PARSER, self, {
                entry.attrib["type"]: entry.text
                for entry in attributes
            })

            properties["checksum"] = checksum
            self.database[checksum] = merge_dictionaries(SKYSCRAPER_DEFAULTS, properties)

    def get_game(self, request):

        resource = self.database.get(request.sha1)

        if resource:
            return ScraperResponse.success(request, resource)

        return ScraperResponse.error(request, self.ID)
