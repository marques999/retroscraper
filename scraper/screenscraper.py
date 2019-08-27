# -*- coding: utf-8 -*-

import operator
import requests

from shared.tools import export
from shared.gdf import GdfFields, GdfRegion

from scraper.thread import ScraperResponse
from scraper.tools import remove_keys, unmagic, parse_datetime

def export_default(context, value):
    return str(value)

def export_integer(context, value):
    return int(value, 10)

def export_rating(context, value):
    return int(value["text"], 10)

def export_field(field):
    return lambda _, value: value[field]

def export_boolean(context, value):
    return value == "1" or value.lower() == "true"

def export_release(context, value):

    return {
        region: parse_datetime(text)
        for region, text in export_regionizable(context, value).items()
    }

SCREENSCRAPER_REGIONS = {
    "de": GdfRegion.GERMANY,
    "asi": GdfRegion.ASIA,
    "au": GdfRegion.AUSTRALIA,
    "br": GdfRegion.BRAZIL,
    "bg": GdfRegion.BULGARIA,
    "ca": GdfRegion.CANADA,
    "cl": GdfRegion.CHILE,
    "cn": GdfRegion.CHINA,
    "ame": GdfRegion.AMERICAS,
    "kr": GdfRegion.KOREA,
    "dk": GdfRegion.DENMARK,
    "sp": GdfRegion.SPAIN,
    "eu": GdfRegion.EUROPE,
    "fi": GdfRegion.FINLAND,
    "fr": GdfRegion.FRANCE,
    "gr": GdfRegion.GREECE,
    "hu": GdfRegion.HUNGARY,
    "il": GdfRegion.ISRAEL,
    "it": GdfRegion.ITALY,
    "jp": GdfRegion.JAPAN,
    "kw": GdfRegion.KUWAIT,
    "wor": GdfRegion.WORLD,
    "mor": GdfRegion.MIDDLE_EAST,
    "no": GdfRegion.NORWAY,
    "nz": GdfRegion.NEW_ZEALAND,
    "oce": GdfRegion.OCEANIA,
    "nl": GdfRegion.NETHERLANDS,
    "pe": GdfRegion.PERU,
    "pl": GdfRegion.POLAND,
    "pt": GdfRegion.PORTUGAL,
    "cz": GdfRegion.CZECH_REPUBLIC,
    "uk": GdfRegion.UNITED_KINGDOM,
    "ru": GdfRegion.RUSSIA,
    "ss": GdfRegion.DEFAULT,
    "sk": GdfRegion.SLOVAKIA,
    "se": GdfRegion.SWEDEN,
    "tw": GdfRegion.TAIWAN,
    "tr": GdfRegion.TURKEY,
    "us": GdfRegion.USA
}

def export_region(context, value):
    return get_region(value["shortname"])

def get_region(region):
    return SCREENSCRAPER_REGIONS.get(region, GdfRegion.UNKNOWN)

def export_regionizable(context, values):
    return dict(map(lambda item: (get_region(item["region"]), item["text"]), values))

def export_localizable(context, values):
    return dict(map(lambda item: (item["langue"], item["text"]), values))

def export_media(context, value):

    return [
        remove_keys(resource, ["crc", "md5", "parent", "url"])
        for resource in value
        if resource["parent"] == "jeu"
    ]


SCREENSCRAPER_GENRES_EXPORTER = {
    GdfFields.ID: ("id", export_integer),
    GdfFields.PARENT: ("parentid", export_integer),
    GdfFields.PRIMARY: ("principale", export_boolean),
    GdfFields.DESCRIPTION: ("noms", export_localizable)
}

def export_genres(context, values):

    return [
        export(SCREENSCRAPER_GENRES_EXPORTER, {}, genre)
        for genre in values
    ]

SCREENSCRAPER_ROM_EXPORTER = {
    GdfFields.ID: ("id", export_integer),
    GdfFields.PARENT: ("romcloneof", export_integer),
    "filename": ("romfilename", export_default),
    "length": ("romsize", export_default),
    "crc32": ("romcrc", export_default),
    "md5": ("romsmd5", export_default),
    "sha1": ("romsha1", export_default),
    "beta": ("beta", export_boolean),
    "demo": ("demo", export_boolean),
    "prototype": ("proto", export_boolean),
    "translation": ("trad", export_boolean),
    "hack": ("hack", export_boolean),
    "unlicensed": ("unl", export_boolean),
    "alternate": ("alt", export_boolean),
    "best": ("best", export_boolean),
    "netplay": ("netplay", export_boolean),
    "region": ("romregions", export_default)
}

def export_rom(context, value):
    return export(SCREENSCRAPER_ROM_EXPORTER, {}, value)

SCREENSCRAPER_PARSER = {
    GdfFields.ID: ("id", export_integer),
    GdfFields.PARENT: ("cloneof", export_integer),
    GdfFields.TITLE: ("noms", export_regionizable),
    GdfFields.REGION: ("regions", export_region),
    GdfFields.PUBLISHER: ("editeur", export_field("text")),
    GdfFields.DEVELOPER: ("developpeur", export_field("text")),
    GdfFields.AGES: ("classifications", export_default),
    GdfFields.PLAYERS: ("joueurs", export_field("text")),
    GdfFields.RATING: ("note", export_rating),
    GdfFields.FAVORITE: ("topstaff", export_boolean),
    GdfFields.DESCRIPTION: ("synopsis", export_localizable),
    GdfFields.RELEASE: ("dates", export_release),
    GdfFields.GENRE: ("genres", export_genres),
    "media": ("medias", export_media),
    "rom": ("rom", export_rom),
    GdfFields.IGNORE: ("notgame", export_boolean)
}

class SkyscraperProvider:

    ID = "screenscraper"
    URL = "https://www.screenscraper.fr/api2"
    APIKEY = "158,211,229,216,192,247,142,172,205,168,210,233,187,208,204,212"

    def __init__(self, platform, username, password):

        self.authentication = {
            "devid": "muldjord",
            "softname": "skyscraper",
            "devpassword": unmagic(self.APIKEY),
            "ssid": username,
            "sspassword": password
        }

        identifier = platform.get("scrapers", {}).get(self.ID, 0)

        if identifier > 0:
            self.authentication["systemeid"] = identifier

    def get_game(self, context):

        response = requests.get(f"{self.URL}/jeuInfos.php", {
            **self.authentication,
            "output": "json",
            "sha1": context.sha1,
            "md5": context.md5,
            "crc32": context.crc32
        })

        if response.status_code != 200:
            return ScraperResponse(context.filename, self.ID)

        json = response.json()["response"]["jeu"]
        metadata = export(SCREENSCRAPER_PARSER, {}, json)

        return ScraperResponse(context.filename, metadata, True)

    def get_media(self, game, media):

        query = {
            **self.authentication,
            "jeuid": game["id"]
        }

        if "region" in media and media["region"] != "ss":
            query["media"] = media["type"] + "(" + media["region"] + ")"
        else:
            query["media"] = media["type"]

        return requests.Request(method="GET",
                                url=f"{self.URL}/mediaJeu.php",
                                params=query).prepare()
