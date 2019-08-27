# -*- coding: utf-8 -*-

import operator
import requests

from scraper.thread import ScraperResponse
from scraper.gdf import GdfFields, GdfRegion
from scraper.tools import export, remove_keys, unmagic, parse_datetime

def export_rating(rating):
    return int(rating["text"], 10)

def export_boolean(value):
    return value == "1" or value.lower() == "true"

def export_release(release_dates):

    return {
        region: parse_datetime(text)
        for region, text in export_regionizable(release_dates).items()
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

def export_region(region):
    return get_region(region["shortname"])

def get_region(region):
    return SCREENSCRAPER_REGIONS.get(region, GdfRegion.UNKNOWN)

def export_regionizable(items):
    return dict(map(lambda item: (get_region(item["region"]), item["text"]), items))

def export_localizable(items):
    return dict(map(lambda item: (item["langue"], item["text"]), items))

def export_media(media):

    return [
        remove_keys(resource, ["crc", "md5", "parent", "url"])
        for resource in media
        if resource["parent"] == "jeu"
    ]

SCREENSCRAPER_GENRES_EXPORTER = {
    GdfFields.ID: ("id", int),
    GdfFields.PARENT: ("parentid", int),
    GdfFields.PRIMARY: ("principale", export_boolean),
    GdfFields.DESCRIPTION: ("noms", export_localizable)
}

def export_genres(genres):

    return [
        export(genre, SCREENSCRAPER_GENRES_EXPORTER)
        for genre in genres
    ]

SCREENSCRAPER_ROM_EXPORTER = {
    GdfFields.ID: ("id", int),
    GdfFields.PARENT: ("romcloneof", int),
    "filename": ("romfilename", str),
    "length": ("romsize", str),
    "crc32": ("romcrc", str),
    "md5": ("romsmd5", str),
    "sha1": ("romsha1", str),
    "beta": ("beta", export_boolean),
    "demo": ("demo", export_boolean),
    "prototype": ("proto", export_boolean),
    "translation": ("trad", export_boolean),
    "hack": ("hack", export_boolean),
    "unlicensed": ("unl", export_boolean),
    "alternate": ("alt", export_boolean),
    "best": ("best", export_boolean),
    "netplay": ("netplay", export_boolean),
    "region": ("romregions", lambda region: region[:region.index(",")])
}

def export_rom(response):
    return export(response, SCREENSCRAPER_ROM_EXPORTER)

SCREENSCRAPER_PARSER = {
    GdfFields.ID: ("id", int),
    GdfFields.PARENT: ("cloneof", int),
    GdfFields.TITLE: ("noms", export_regionizable),
    GdfFields.REGION: ("regions", export_region),
    GdfFields.PUBLISHER: ("editeur", operator.itemgetter("text")),
    GdfFields.DEVELOPER: ("developpeur", operator.itemgetter("text")),
    GdfFields.AGES: ("classifications", str),
    GdfFields.PLAYERS: ("joueurs", operator.itemgetter("text")),
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
        metadata = export(json, SCREENSCRAPER_PARSER)

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
