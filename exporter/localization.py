# -*- coding: utf-8 -*-

from operator import itemgetter
from shared.gdf import GdfFields

def merge_dictionaries(*collections):

    result = {}

    for collection in collections:
        result.update(collection.copy())

    return result

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
