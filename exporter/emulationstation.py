# -*- coding: utf-8 -*-

from pathlib import PurePath
from datetime import datetime
from xml.etree import ElementTree

from exporter.gdf import EsFields, GdfFields
from exporter.tools import export, prettify_xml, export_media

class EsExporter:

    @staticmethod
    def export_string(context, value):
        return value

    @staticmethod
    def export_kidgame(context, value):
        return 1 <= int(value) <= 10

    @staticmethod
    def export_players(context, value):
        return value[value.rfind("-") + 1:]

    @staticmethod
    def export_releasedate(context, value):
        return value.strftime("%Y%m%dT%H%M%S")

    @staticmethod
    def export_path(context, value):
        return str(context["content_directory"] / (value + ".a52"))

    ESGAME_MAPPER = {
        EsFields.PATH: (GdfFields.CHECKSUM, export_path),
        EsFields.NAME: (GdfFields.TITLE, export_string),
        EsFields.IMAGE: (GdfFields.SCREENSHOT, export_media),
        EsFields.WHEEL: (GdfFields.WHEEL, export_media),
        EsFields.MARQUEE: (GdfFields.MARQUEE, export_media),
        EsFields.VIDEO: (GdfFields.VIDEO, export_media),
        EsFields.RATING: (GdfFields.RATING, export_string),
        EsFields.DESC: (GdfFields.DESCRIPTION, export_string),
        EsFields.RELEASEDATE: (GdfFields.RELEASE, export_string),
        EsFields.DEVELOPER: (GdfFields.DEVELOPER, export_string),
        EsFields.PUBLISHER: (GdfFields.PUBLISHER, export_string),
        EsFields.GENRE: (GdfFields.GENRE, export_string),
        EsFields.PLAYERS: (GdfFields.PLAYERS, export_players),
        EsFields.KIDGAME: (GdfFields.AGES, export_kidgame),
    }

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
        esgame = export(ESGAME_MAPPER, self, entry)

        for (key, value) in esgame.items():
            ElementTree.SubElement(root, key).text = value
