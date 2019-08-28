# -*- coding: utf-8 -*-

import os
import gzip

from hashlib import sha1
from xml.dom import minidom
from zipfile import ZipFile
from operator import itemgetter
from xml.etree import ElementTree

from shared.gdf import GdfFields
from shared.tools import merge_dictionaries

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

def sort_genres(genres):

    return (
        int(genres[GdfFields.PARENT] != "0"),
        int(genres[GdfFields.PRIMARY]),
        genres[GdfFields.ID]
    )

def export_media(media):

    def export_media_private(context, resource):

        destination = media / os.path.basename()

        if not context.relative:
            destination = context.output_directory / destination

        return (str(context.media_directory / resource), str(destination))

    return export_media_private

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

def __merge_dictionary(path, source, destination):

    for key, value in destination.items():

        if key in source:
            source[key] = __merge_recursive(path + [key], source[key], value)
        else:
            source[key] = value

    return source

def __merge_recursive(path, source, destination):

    if not (isinstance(source, type(destination)) or isinstance(destination, type(source))):
        return destination
    elif isinstance(destination, dict):
        return __merge_dictionary(path, source, destination)
    elif isinstance(destination, list):
        return source + destination
    else:
        return destination

def merge(source, destination):

    return __merge_recursive([], source, destination)
