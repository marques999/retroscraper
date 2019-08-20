from re import sub
from os import path
from tools import parse_datetime
from textwrap import TextWrapper, dedent
from itertools import takewhile

def export_string(context, value):
    return value

def export_rating(context, value):
    return "{0:.0%}".format(float(value))

def export_players(context, value):
    return value[value.rfind("-") + 1:]

def export_release(context, value):
    return parse_datetime(value).strftime("%Y-%m-%d")

def export_rom(context, value):
    return str(context["roms_directory"] / value).replace("\\", "/")

def export_media(context, value):
    return str(context["media_directory"] / value).replace("\\", "/")

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

class PegasusMetadata:

    def __init__(self, context):

        self.context = context

    def debug(self, entries):

        return self.__generate_metadata(entries)

    def write(self, entries, path):

        filename = path / "metadata.pegasus.txt"

        with open(filename, mode="w", encoding="utf-8") as stream:
            stream.write(self.__generate_metadata(entries))

    def __generate_metadata(self, entries):

        return "\n\n\n".join(map(self.__generate_entry, entries))

    def __generate_entry(self, entry):

        return "\n".join(
            "%s: %s" % (destination, exporter(self.context, entry[source]))
            for destination, (source, exporter) in PEGASUS_EXPORTER.items()
            if source in entry
        )

# metadata_filename = "D:\\Atari 7800 [US]\\metadata.pegasus.txt"

# with open(metadata_filename, mode="r", encoding="utf-8") as stream:
#     contents = stream.read().split("\n\n\n")
#     entries = iter(contents[0].split("\n"))
#     mapping = {}
#     while entries:
#         key, _, value = next(entries, "").partition(": ")
#         if key == "description":
#             print(list(takewhile(lambda x: x.startswith("  "), entries)))
#         else:
#             mapping[key] = value

#     print(mapping)
