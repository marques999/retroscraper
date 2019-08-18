from itertools import groupby
from xml.etree import ElementTree

def read_database(cache_directory):

    database = {}
    root = ElementTree.parse(cache_directory / "db.xml").getroot()

    resources = groupby(
        sorted(root, key=lambda entry: entry.attrib["sha1"]),
        key=lambda entry: entry.attrib["sha1"]
    )

    for (checksum, properties) in resources:

        database[checksum] = {
            entry.attrib["type"]: entry.text
            for entry in properties
        }

    return database
