from re import compile
from gdf import GdfFields
from datetime import datetime

def group_by_region(items):
    return to_dictionary(items, "region")

def group_by_language(items):
    return to_dictionary(items, "langue")

def parse_boolean(value):
    return value == "1" or value.lower() == "true"

def to_dictionary(items, key):
    return dict(map(lambda item: (item[key], item["text"]), items))

def without_keys(collection, keys):

     return dict(filter(
         lambda pair: pair[0] not in keys,
         collection.items()
     ))

def execute_pipeline(response, keys, handlers):

    return {
        destination: handlers[destination](response[source])
        if destination in handlers
        else response[source]
        for (source, destination) in keys.items()
        if source in response
    }

def parse_media(media):

    return [
        without_keys(resource, ["crc", "md5", "parent", "url"])
        for resource in media
        if resource["parent"] == "jeu"
    ]

DATETIME_REGEX = [
    compile("^\\d{4}$"),
    compile("^\\d{4}-[0-1]{1}\\d{1}$"),
    compile("^\\d{4}-[0-1]{1}\\d{1}-[0-3]{1}\\d{1}$"),
    compile("^[0-1]{1}\\d{1}/[0-3]{1}\\d{1}/\\d{4}$"),
    compile("^\\d{4}-[a-zA-Z]{3}-[0-3]{1}\\d{1}$"),
    compile("^[a-zA-z]{3}, \\d{4}$"),
    compile("^[a-zA-z]{3} ([0-3]{1})?\\d{1}, \\d{4}$")
]

DATETIME_FORMAT = [
    "%Y",
    "%Y-%m",
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%Y-%M-%d",
    "%M, %Y",
    "%M %d, %Y"
]

def parse_datetime(timestamp: str) -> datetime:

    for index, regex in enumerate(DATETIME_REGEX):
        if regex.search(timestamp):
            return datetime.strptime(timestamp, DATETIME_FORMAT[index])

    return datetime.now()

GENRE_KEYS = {
    "id": "id",
    "principale": "primary",
    "parentid": "parent",
    "noms": "description"
}

GENRE_HANDLERS = {
    "id": int,
    "parent": int,
    "primary": parse_boolean,
    "description": group_by_language
}

def parse_genres(response):

    return [
        execute_pipeline(genre, GENRE_KEYS, GENRE_HANDLERS)
        for genre in response
    ]

ROM_KEYS = {
    "id": "id",
    "romfilename": "filename",
    "romregions": "region",
    "romsize": "size",
    "romcrc": "crc32",
    "romsmd5": "md5",
    "romsha1": "sha1",
    "romcloneof": "parent",
    "beta": "beta",
    "demo": "demo",
    "proto": "prototype",
    "trad": "translation",
    "hack": "hack",
    "unl": "unlicensed",
    "alt": "alternate",
    "best": "best",
    "netplay": "netplay"
}

ROM_HANDLERS = {
    "id": int,
    "parent": int,
    "beta": parse_boolean,
    "demo": parse_boolean,
    "proto": parse_boolean,
    "translation": parse_boolean,
    "hack": parse_boolean,
    "prototype": parse_boolean,
    "unlicensed": parse_boolean,
    "alternate": parse_boolean,
    "best": parse_boolean,
    "netplay": parse_boolean,
    "region": lambda region: region[:region.index(",")]
}

METADATA_KEYS = {
    "id": "id",
    "notgame": "hidden",
    "noms": "title",
    "regions": "region",
    "cloneof": "parent",
    "systemeid": "platform",
    "editeur": GdfFields.PUBLISHER,
    "developpeur": GdfFields.DEVELOPER,
    "joueurs": GdfFields.PLAYERS,
    "note": "ages",
    "topstaff": "favorite",
    "synopsis": GdfFields.DESCRIPTION,
    "dates": GdfFields.RELEASE,
    "genres": GdfFields.GENRE,
    "medias": "media",
    "rom": "rom"
}

def localize_text(items, language, region):
    return items["text"]

def localize_region(items, language, region):
    return items[region]

def localize_language(items, language, region):
    return items[language]

def parse_rom(response):
    return execute_pipeline(response, ROM_KEYS, ROM_HANDLERS)

def parse_metadata(response):
    return execute_pipeline(response, METADATA_KEYS, METADATA_HANDLERS)

def localize_genres(items, language, region):

    for genre in items:
        genre["description"] = localize_language(genre["description"], language, region)

LOCALIZE_HANDLERS = {
    "developer": localize_text,
    "publisher": localize_text,
    "genres": localize_genres,
    "title": localize_region,
    "description": localize_language,
    "releasedate": localize_region
}

def localize_metadata(response, language, region):

    localizations = {
        destination: handler(response[destination], language, region)
        for (destination, handler) in LOCALIZE_HANDLERS.items()
        if destination in response
    }

    response.update(localizations)

METADATA_HANDLERS = {
    "id": int,
    "platform": int,
    "rom": parse_rom,
    "media": parse_media,
    "genres": parse_genres,
    "hidden": parse_boolean,
    "title": group_by_region,
    "favorite": parse_boolean,
    "releasedate": group_by_region,
    "description": group_by_language,
    "ages": lambda value: value["text"],
    "players": lambda value: value["text"],
    "region": lambda value: value["shortname"],
}
