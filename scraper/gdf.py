# -*- coding: utf-8 -*-

from operator import itemgetter
from scraper.tools import merge_dictionaries

class GdfRegion:
    GERMANY = 115
    ASIA = 114
    AUSTRALIA = 61
    BRAZIL = 63
    BULGARIA = 3891
    CANADA = 121
    CHILE = 3822
    CHINA = 56
    AMERICAS = 3257
    KOREA = 58
    DENMARK = 282
    SPAIN = 122
    EUROPE = 48
    FINLAND = 283
    FRANCE = 45
    GREECE = 3892
    HUNGARY = 3821
    ISRAEL = 3827
    ITALY = 118
    JAPAN = 47
    KUWAIT = 3832
    WORLD = 57
    MIDDLE_EAST = 3826
    NORWAY = 3884
    NEW_ZEALAND = 3825
    OCEANIA = 3824
    NETHERLANDS = 130
    PERU = 3828
    POLAND = 3595
    PORTUGAL = 3780
    CZECH_REPUBLIC = 3820
    UNITED_KINGDOM = 3289
    RUSSIA = 126
    DEFAULT = 20240
    SLOVAKIA = 3823
    SWEDEN = 116
    TAIWAN = 112
    TURKEY = 3829
    USA = 46
    UNKNOWN = 3603

class GdfFields:
    ID = "id"
    TITLE = "title"
    PARENT = "parent"
    REGION = "region"
    PRIMARY = "primary"
    IGNORE = "ignore"
    DEVELOPER = "developer"
    PUBLISHER = "publisher"
    GENRE = "genre"
    AGES = "ages"
    DESCRIPTION = "description"
    RELEASE = "releasedate"
    PLAYERS = "players"
    FAVORITE = "favorite"
    RATING = "rating"
    CHECKSUM = "checksum"

def localize_genres(items, language, region):

    for genre in items:
        genre[GdfFields.DESCRIPTION] = genre[GdfFields.DESCRIPTION][language]

def localize(response, language, region):

    LOCALIZERS = {
        GdfFields.GENRE: localize_genres,
        GdfFields.TITLE: itemgetter(region),
        GdfFields.RELEASE: itemgetter(region),
        GdfFields.DESCRIPTION: itemgetter(language)
    }

    return merge_dictionaries(response, {
        destination: handler(response[destination], language, region)
        for (destination, handler) in LOCALIZERS.items()
        if destination in response
    })
