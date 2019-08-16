from datetime import datetime
from xml.etree import ElementTree
from gdf import EsFields, GdfFields

def export_string(context, value):
    return value

def export_kidgame(context, value):
    return 1 <= int(value) <= 10

def export_players(context, value):
    return value[value.rfind("-") + 1:]

def export_releasedate(context, value):
    return value.strftime("%Y%m%dT%H%M%S")

def export_image(context, value):
    return str(context["media_directory"] / (value + ".png"))

def export_path(context, value):
    return str(context["content_directory"] / (value + ".a52"))

ESGAME_EXPORTER = {
    EsFields.PATH: (GdfFields.CHECKSUM, export_path),
    EsFields.NAME: (GdfFields.TITLE, export_string),
    EsFields.IMAGE: (GdfFields.CHECKSUM, export_image),
    EsFields.RATING: (GdfFields.RATING, export_string),
    EsFields.DESC: (GdfFields.DESCRIPTION, export_string),
    EsFields.RELEASEDATE: (GdfFields.RELEASE, export_string),
    EsFields.DEVELOPER: (GdfFields.DEVELOPER, export_string),
    EsFields.PUBLISHER: (GdfFields.PUBLISHER, export_string),
    EsFields.GENRE: (GdfFields.GENRE, export_string),
    EsFields.PLAYERS: (GdfFields.PLAYERS, export_players),
    EsFields.KIDGAME: (GdfFields.AGES, export_kidgame),
}

class EsExporter:

    def __init__(self, content_directory):

        self.context = {
            "content_directory": content_directory,
            "media_directory": content_directory / "media"
        }

    def generate_esgamelist(self, entries):

        esgamelist_root = ElementTree.Element("gameList")

        for entry in entries:
            self.__generate_entry(esgamelist_root, entry)

        return ElementTree.dump(esgamelist_root)

    def __generate_entry(self, root, entry):

        esgame_root = ElementTree.SubElement(root, "game")

        for destination, (source, handler) in ESGAME_EXPORTER.items():

            if source in entry:
                element = ElementTree.SubElement(esgame_root, destination)
                element.text = handler(self.context, entry[source])
