# -*- coding: utf-8 -*-

from re import compile
from zlib import crc32
from hashlib import md5, sha1
from datetime import datetime
from scraper.thread import ScraperContext

YEOCHIN = bytearray("널향한설레임을오늘부터우리는꿈꾸며기도하는오늘부터우리는", "utf-8")

def remove_keys(collection, keys):

     return dict(filter(
         lambda pair: pair[0] not in keys, collection.items()
    ))

def merge_dictionaries(*collections):

    result = {}

    for collection in collections:
        result.update(collection.copy())

    return result

def export(metadata, exporter):

    return dict(
        (destination, exporter(metadata[source]))
        for destination, (source, exporter) in exporter.items()
        if source in metadata
    )

def unmagic(contents):

    return "".join(
        chr(int(lhs) ^ rhs)
        for lhs, rhs in zip(contents.split(","), YEOCHIN)
    )

DATETIME_REGEX = [
    ("%Y", compile("^\\d{4}$")),
    ("%Y-%m", compile("^\\d{4}-[0-1]{1}\\d{1}$")),
    ("%Y-%m-%d", compile("^\\d{4}-[0-1]{1}\\d{1}-[0-3]{1}\\d{1}$")),
    ("%m/%d/%Y", compile("^[0-1]{1}\\d{1}/[0-3]{1}\\d{1}/\\d{4}$")),
    ("%Y-%M-%d", compile("^\\d{4}-[a-zA-Z]{3}-[0-3]{1}\\d{1}$")),
    ("%M, %Y", compile("^[a-zA-z]{3}, \\d{4}$")),
    ("%M %d, %Y", compile("^[a-zA-z]{3} ([0-3]{1})?\\d{1}, \\d{4}$"))
]

def parse_datetime(timestamp):

    for formatter, regex in DATETIME_REGEX:
        if regex.search(timestamp):
            return int(datetime.strptime(timestamp, formatter).timestamp())

    return datetime.now()

def generate_digest(filename):

    with open(filename, "rb") as stream:

        contents = stream.read()

        return ScraperContext(
            filename,
            hex(crc32(contents))[2:],
            md5(contents).hexdigest(),
            sha1(contents).hexdigest()
        )
