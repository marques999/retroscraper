# -*- coding: utf-8 -*-

from pathlib import PurePath
from datetime import datetime
from xml.etree import ElementTree

from shared import handlers
from shared.tools import export
from shared.gdf import GdfFields

from exporter.tools import prettify_xml, export_media

class EsFields(object):

    NAME = "name",
    PATH = "path"
    RATING = "rating"
    DESC = "desc"
    IMAGE = "image"
    RELEASEDATE = "releasedate"
    DEVELOPER = "developer"
    PUBLISHER = "publisher"
    GENRE = "genre"
    PLAYERS = "players"
    KIDGAME = "kidgame"
    WHEEL = "wheel"
    MARQUEE = "marquee"
    VIDEO = "video"

def export_kidgame(context, value):
    return 1 <= int(value) <= 10

def export_players(context, value):
    return value[value.rfind("-") + 1:]

def export_path(context, value):
    return str(context["content_directory"] / (value + ".a52"))

EMULATIONSTATION_EXPORTER = {
    EsFields.PATH: (GdfFields.CHECKSUM, export_path),
    EsFields.NAME: (GdfFields.TITLE, handlers.string),
    EsFields.IMAGE: (GdfFields.SCREENSHOT, export_media),
    EsFields.WHEEL: (GdfFields.WHEEL, export_media),
    EsFields.MARQUEE: (GdfFields.MARQUEE, export_media),
    EsFields.VIDEO: (GdfFields.VIDEO, export_media),
    EsFields.RATING: (GdfFields.RATING, handlers.string),
    EsFields.DESC: (GdfFields.DESCRIPTION, handlers.string),
    EsFields.RELEASEDATE: (GdfFields.RELEASE, handlers.timestamp("%Y%m%dT%H%M%S")),
    EsFields.DEVELOPER: (GdfFields.DEVELOPER, handlers.string),
    EsFields.PUBLISHER: (GdfFields.PUBLISHER, handlers.string),
    EsFields.GENRE: (GdfFields.GENRE, handlers.string),
    EsFields.PLAYERS: (GdfFields.PLAYERS, export_players),
    EsFields.KIDGAME: (GdfFields.AGES, export_kidgame),
}

class EsExporter(object):

    def __init__(self):

        self.context = context

    def debug(self, entries):

        return prettify_xml(self.__generate_metadata(entries), "  ")

    def write(self, entries, path):

        filename = path / "gamelist.xml"

        with open(filename, mode="w", encoding="utf-8") as stream:
            stream.write(prettify_xml(self.__generate_metadata(entries), "\t"))

    def __generate_metadata(self, entries):

        root = ElementTree.Element("gameList")

        for entry in entries:
            self.__generate_entry(root, entry)

        return ElementTree.dump(root)

    def __generate_entry(self, root, entry):

        root = ElementTree.SubElement(root, "game")
        esgame = export(EMULATIONSTATION_EXPORTER, self, entry)

        for (key, value) in esgame.items():
            ElementTree.SubElement(root, key).text = value
