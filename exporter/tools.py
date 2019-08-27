# -*- coding: utf-8 -*-

import os
import re
import gzip

from hashlib import sha1
from xml.dom import minidom
from zipfile import ZipFile
from pathlib import PurePath
from datetime import datetime
from xml.etree import ElementTree

DATETIME_REGEX = [
    (re.compile("^\\d{4}$"), "%Y"),
    (re.compile("^\\d{4}-[0-1]{1}\\d{1}$"), "%Y-%m"),
    (re.compile("^\\d{4}-[0-1]{1}\\d{1}-[0-3]{1}\\d{1}$"), "%Y-%m-%d"),
    (re.compile("^[0-1]{1}\\d{1}/[0-3]{1}\\d{1}/\\d{4}$"), "%m/%d/%Y"),
    (re.compile("^\\d{4}-[a-zA-Z]{3}-[0-3]{1}\\d{1}$"), "%Y-%M-%d"),
    (re.compile("^[a-zA-z]{3}, \\d{4}$"), "%M, %Y"),
    (re.compile("^[a-zA-z]{3} ([0-3]{1})?\\d{1}, \\d{4}$"), "%M %d, %Y")
]

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

def parse_datetime(timestamp):

    for (regex, formatter) in DATETIME_REGEX:
        if regex.search(timestamp):
            return datetime.strptime(timestamp, formatter)

    return datetime.now()

def export(exporter, context, entry):

     return (
         (destination, exporter(context, entry[source]))
         for destination, (source, exporter) in exporter.items()
         if source in entry
     )

def get_files(directory, extensions):

    return (
        os.path.join(root, filename)
        for root, _, filenames in os.walk(directory)
        for filename in filenames
        if not extensions or os.path.splitext(filename)[-1].lower() in extensions
    )

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
