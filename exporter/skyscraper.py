# -*- coding: utf-8 -*-

from datetime import datetime
from itertools import groupby
from operator import attrgetter
from xml.etree import ElementTree
from exporter.tools import prettify_xml

class SkyscraperExporter:

    def __init__(self, context):

        self.context = context

    def debug(self, entries):

        return prettify_xml(self.__generate_metadata(entries), "  ")

    def write(self, path, entries):

        with open(path / "db.xml", mode="w", encoding="utf-8") as stream:
            stream.write(prettify_xml(self.__generate_metadata(entries), "\t"))

    def __generate_metadata(self, entries):

        timestamp = datetime.now()
        skyscraper_root = ElementTree.Element("resources")

        for (checksum, entry) in entries.items():

            attributes = {
                "sha1": checksum,
                "source": "screenscraper",
                "timestamp": str(round(timestamp.timestamp()))
            }

            for (key, value) in entry.items():

                ElementTree.SubElement(skyscraper_root, "resource", {
                    **attributes,
                    "type": key
                }).text = value

        return skyscraper_root

class SkyscraperImporter:

    def __init__(self, context):

        self.context = context

    def read(self, path):

        gamedb = {}
        root = ElementTree.parse(path / "db.xml").getroot()
        entries = sorted(root, key=lambda entry: entry.attrib["sha1"])
        groups = groupby(entries, key=lambda entry: entry.attrib["sha1"])

        for (checksum, attributes) in groups:

            properties = {
                entry.attrib["type"]: entry.text
                for entry in attributes
            }

            properties["checksum"] = checksum
            gamedb[checksum] = properties

        return gamedb
