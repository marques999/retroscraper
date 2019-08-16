from gdf import GdfFields, PegasusFields
from textwrap import TextWrapper, dedent

def export_string(context, value):
    return value

def export_rating(context, value):
    return "{0:.0} %".format(value)

def export_release(context, value):
    return value.strftime("%Y-%m-%d")

def export_players(context, value):
    return value[value.rfind("-") + 1:]

def export_file(context, value):
    return str(context["content_directory"] / (value + ".a52"))

def export_description(context, value):
    return TextWrapper(width=80).fill(dedent(value)).join("\n\t")

def export_media(directory):
    return lambda context, value: str(context["media_directory"] / directory / (value + ".png"))

PEGASUS_EXPORTER = {
    PegasusFields.GAME: (GdfFields.TITLE, export_string),
    PegasusFields.FILE: (GdfFields.CHECKSUM, export_file),
    PegasusFields.RATING: (GdfFields.RATING, export_rating),
    PegasusFields.DESCRIPTION: (GdfFields.DESCRIPTION, export_description),
    PegasusFields.RELEASE: (GdfFields.RELEASE, export_string),
    PegasusFields.DEVELOPER: (GdfFields.DEVELOPER, export_string),
    PegasusFields.PUBLISHER: (GdfFields.PUBLISHER, export_string),
    PegasusFields.GENRE: (GdfFields.GENRE, export_string),
    PegasusFields.PLAYERS: (GdfFields.PLAYERS, export_players),
    PegasusFields.ASSETS_SCREENSHOT: (GdfFields.CHECKSUM, export_media("screenshots")),
    PegasusFields.ASSETS_BOXFRONT: (GdfFields.CHECKSUM, export_media("covers")),
    PegasusFields.ASSETS_MARQUEE: (GdfFields.CHECKSUM, export_media("marquees")),
    PegasusFields.ASSETS_WHEEL: (GdfFields.CHECKSUM, export_media("wheels")),
    PegasusFields.ASSETS_VIDEO: (GdfFields.CHECKSUM, export_media("videos"))
}

class PegasusExporter:

    def __init__(self, content_directory):

        self.context = {
            "content_directory": content_directory,
            "media_directory": content_directory / "media"
        }

    def generate_pegasus(self, entries):

        return "\n\n".join(map(self.__generate_pegasus, entries))

    def __generate_pegasus(self, entry):

        return "\n".join(
            "%s: %s" % (destination, handler(self.context, entry[source]))
            for destination, (source, handler) in PEGASUS_EXPORTER.items()
            if source in entry
        )
