# -*- coding: utf-8 -*-

import operator
import requests

from shared import handlers
from shared.gdf import GdfFields, GdfRegions
from shared.tools import export, parse_datetime

from threading import BoundedSemaphore

from scraper.thread import ScraperResponse
from scraper.tools import remove_keys, unmagic

def export_rating(context, value):
    return int(value["text"], 10)

def export_field(field):
    return lambda _, value: value[field]

def export_boolean(context, value):
    return value == "1" or value.lower() == "true"

def export_release(context, value):

    return {
        region: parse_datetime(context, text)
        for region, text in export_regionizable(context, value).items()
    }

SCREENSCRAPER_REGIONS = {
    "de": GdfRegions.GERMANY,
    "asi": GdfRegions.ASIA,
    "au": GdfRegions.AUSTRALIA,
    "br": GdfRegions.BRAZIL,
    "bg": GdfRegions.BULGARIA,
    "ca": GdfRegions.CANADA,
    "cl": GdfRegions.CHILE,
    "cn": GdfRegions.CHINA,
    "ame": GdfRegions.AMERICAS,
    "kr": GdfRegions.KOREA,
    "dk": GdfRegions.DENMARK,
    "sp": GdfRegions.SPAIN,
    "eu": GdfRegions.EUROPE,
    "fi": GdfRegions.FINLAND,
    "fr": GdfRegions.FRANCE,
    "gr": GdfRegions.GREECE,
    "hu": GdfRegions.HUNGARY,
    "il": GdfRegions.ISRAEL,
    "it": GdfRegions.ITALY,
    "jp": GdfRegions.JAPAN,
    "kw": GdfRegions.KUWAIT,
    "wor": GdfRegions.WORLD,
    "mor": GdfRegions.MIDDLE_EAST,
    "no": GdfRegions.NORWAY,
    "nz": GdfRegions.NEW_ZEALAND,
    "oce": GdfRegions.OCEANIA,
    "nl": GdfRegions.NETHERLANDS,
    "pe": GdfRegions.PERU,
    "pl": GdfRegions.POLAND,
    "pt": GdfRegions.PORTUGAL,
    "cz": GdfRegions.CZECH_REPUBLIC,
    "uk": GdfRegions.UNITED_KINGDOM,
    "ru": GdfRegions.RUSSIA,
    "ss": GdfRegions.WORLD,
    "sk": GdfRegions.SLOVAKIA,
    "se": GdfRegions.SWEDEN,
    "tw": GdfRegions.TAIWAN,
    "tr": GdfRegions.TURKEY,
    "us": GdfRegions.USA
}

def export_region(context, value):
    return get_region(value["shortname"])

def get_region(region):
    return SCREENSCRAPER_REGIONS.get(region, GdfRegions.UNKNOWN)

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

SCREENSCRAPER_GENRES = {
    GdfFields.ID: ("id", handlers.integer),
    GdfFields.PARENT: ("parentid", handlers.integer),
    GdfFields.PRIMARY: ("principale", export_boolean),
    GdfFields.DESCRIPTION: ("noms", export_localizable)
}

def export_genres(context, values):

    return [
        export(SCREENSCRAPER_GENRES, {}, genre)
        for genre in values
    ]

SCREENSCRAPER_ROM = {
    GdfFields.ID: ("id", handlers.integer),
    GdfFields.PARENT: ("romcloneof", handlers.integer),
    "filename": ("romfilename", handlers.string),
    "length": ("romsize", handlers.string),
    "crc32": ("romcrc", handlers.string),
    "md5": ("romsmd5", handlers.string),
    "sha1": ("romsha1", handlers.string),
    "beta": ("beta", export_boolean),
    "demo": ("demo", export_boolean),
    "prototype": ("proto", export_boolean),
    "translation": ("trad", export_boolean),
    "hack": ("hack", export_boolean),
    "unlicensed": ("unl", export_boolean),
    "alternate": ("alt", export_boolean),
    "best": ("best", export_boolean),
    "netplay": ("netplay", export_boolean),
    "region": ("romregions", handlers.string)
}

def export_rom(context, value):
    return export(SCREENSCRAPER_ROM, {}, value)

SCREENSCRAPER_PARSER = {
    GdfFields.ID: ("id", handlers.integer),
    GdfFields.PARENT: ("cloneof", handlers.integer),
    GdfFields.TITLE: ("noms", export_regionizable),
    GdfFields.REGION: ("regions", export_region),
    GdfFields.PUBLISHER: ("editeur", export_field("text")),
    GdfFields.DEVELOPER: ("developpeur", export_field("text")),
    GdfFields.AGES: ("classifications", handlers.string),
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

def parse_integer(value):

    try:
        return int(value)
    except ValueError:
        return 0

def parse_response(response):

    if response.status_code != 200:
        return None, response.content

    json = response.json()
    header = json.get("header", {})

    if header.get("success", "false") == "true" and "response" in json:
        return json["response"], None
    else:
        return None, header["error"]

class ScreenscraperProvider:

    ID = "screenscraper"
    URL = "https://www.screenscraper.fr/api2"
    API_KEY = "158,211,229,216,192,247,142,172,205,168,210,233,187,208,204,212"

    def __init__(self, platform, username, password):

        self.authentication = {
            "softname": "skyscraper",
            "devid": "muldjord",
            "devpassword": unmagic(self.API_KEY),
            "ssid": username,
            "sspassword": password
        }

        self.blocked = False
        threads = self.__get_limits()
        self.__semaphore = BoundedSemaphore(threads)
        identifier = platform.get("scrapers", {}).get(self.ID, 0)

        if identifier > 0:
            self.authentication["systemeid"] = identifier

    def __get_limits(self):

        response, error = parse_response(requests.get(f"{self.URL}/ssuserInfos.php", {
            "output": "json",
            **self.authentication
        }))

        return 1 if error else parse_integer(response["ssuser"]["maxthreads"])

    def get_game(self, context):

        if self.blocked:
            return ScraperResponse.error(context, self.ID)

        query = {
            "output": "json",
            **self.authentication,
            "md5": context.md5,
            "sha1": context.sha1,
            "crc32": context.crc32
        }

        self.__semaphore.acquire()
        response, error = parse_response(requests.get(f"{self.URL}/jeuInfos.php", query))
        self.__semaphore.release()

        if error:
            return ScraperResponse.error(context, error)

        ssuser = response["ssuser"]
        metadata = export(SCREENSCRAPER_PARSER, {}, response["jeu"])

        if parse_integer(ssuser["requeststoday"]) >= parse_integer(ssuser["maxrequestsperday"]):
            self.blocked = True

        return ScraperResponse.success(context, metadata)

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
