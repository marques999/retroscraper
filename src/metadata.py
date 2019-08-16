from xml.dom import minidom
from itertools import groupby
from xml.etree import ElementTree
from pathlib import Path, PurePosixPath
from emulationstation import EsExporter

def sort_sha1(resource):

    return resource.attrib["sha1"]

def get_user_directory(configuration):

    if configuration["retropie"]:
        return PurePosixPath("/home", "pi")
    else:
        return Path.home()

def get_skyscraper_directory(configuration):

    return Path.home() / ".skyscraper" / "cache" / configuration["platform"]

def get_retropie_directory(configuration):

    return get_user_directory(configuration) / "RetroPie" / "roms" / configuration["platform"]

def read_skyscraper_db(configuration):

    database = {}
    skyscraper_directory = get_skyscraper_directory(configuration)
    tree = ElementTree.parse(skyscraper_directory / "db.xml")
    resources = sorted(tree.getroot(), key=sort_sha1)

    for (checksum, properties) in groupby(resources, key=sort_sha1):

        entries = {
            entry.attrib["type"]: entry.text
            for entry in properties
        }

        database[checksum] = {
            **entries,
            "checksum": checksum
        }

    return sorted(
        database.values(),
        key=lambda entry: entry["title"]
    )

def write_xml(filename, root):

    xml_raw = ElementTree.tostring(root, "utf-8")
    xml_reparsed = minidom.parseString(xml_raw)

    with open(filename, "w", encoding="utf-8") as stream:
        stream.write(xml_reparsed.toprettyxml(indent="\t"))

if __name__ == "__main__":

    settings = {
        "retropie": True,
        "platform": "atari5200"
    }

    gamedb = read_skyscraper_db(settings)
    retropie_directory = get_retropie_directory(settings)
    write_xml(EsExporter(retropie_directory).generate_esgamelist(gamedb))
