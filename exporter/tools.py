# -*- coding: utf-8 -*-

import os
import gzip

from hashlib import sha1
from xml.dom import minidom
from zipfile import ZipFile
from operator import itemgetter
from shared.gdf import GdfFields
from xml.etree import ElementTree

def get_sha1(stream):

    return sha1(stream).hexdigest().lower()

def prettify_xml(root, separator):

    return minidom.parseString(
        ElementTree.tostring(root)
    ).toprettyxml(indent=separator)

def digest_file(filename):

    with open(filename, "rb") as stream:
        return get_sha1(stream.read())

def digest_gzip(filename):

    with gzip.open(filename, "r") as stream:
        return get_sha1(stream.read())

def digest_zip(filename):

    with ZipFile(filename, "r") as zipfile:
        for entry in zipfile.infolist():
            return get_sha1(zipfile.read(entry))

    return get_sha1(filename)

def get_roms(roms_directory, extensions):

    roms = {}

    filenames = (
        os.path.join(root, filename)
        for root, _, filenames in os.walk(roms_directory)
        for filename in filenames
    )

    for filename in filenames:

        extension = os.path.splitext(filename)[-1].lower()

        if extension == ".zip":
            roms[digest_zip(filename)] = filename
        elif extension == ".gz":
            roms[digest_gzip(filename)] = filename
        elif extension not in extensions:
            continue

        roms[digest_file(filename)] = filename

    return roms

def export_media(context, media, resource):

    return (
        context["media_directory"] / resource,
        context["output_directory"] / media / os.path.basename(resource)
    )

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
