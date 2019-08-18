from re import sub
from os import path
from pathlib import PurePath
from tools import parse_datetime
from textwrap import TextWrapper, dedent

def export_string(context, value):
    return value

def export_rating(context, value):
    return "{0:.0%}".format(float(value))

def export_players(context, value):
    return value[value.rfind("-") + 1:]

def export_release(context, value):
    return parse_datetime(value).strftime("%Y-%m-%d")

def export_rom(context, value):
    return str(context.roms_directory / value).replace("\\", "/")

def export_media(context, value):
    return str(context.media_directory / value).replace("\\", "/")

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
    "game": ("title", export_string),
    "file": ("path", export_rom),
    "developer": ("developer", export_string),
    "publisher": ("publisher", export_string),
    "genre": ("tags", export_string),
    "description": ("description", export_description),
    "release": ("releasedate", export_release),
    "players": ("players", export_players),
    "rating": ("rating", export_rating),
    "assets.boxfront": ("cover", export_media),
    "assets.screenshots": ("screenshot", export_media),
    "assets.wheel": ("wheel", export_media),
}

class PegasusExporter:

    def __init__(self, context):

        self.context = context

    def generate_metadata(self, entries):

        return "\n\n\n".join(map(self.__generate_entry, entries))

    def write_metadata(self, entries, directory):

        metadata_filename = path.join(directory, "metadata.pegasus.txt")

        with open(metadata_filename, "w", encoding="utf-8") as stream:
            stream.write(self.generate_metadata(entries))

    def __generate_entry(self, entry):

        return "\n".join(
            "%s: %s" % (destination, handler(self.context, entry[source]))
            for destination, (source, handler) in PEGASUS_EXPORTER.items()
            if source in entry
        )
