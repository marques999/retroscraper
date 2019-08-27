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

def unmagic(contents):

    return "".join(
        chr(int(lhs) ^ rhs)
        for lhs, rhs in zip(contents.split(","), YEOCHIN)
    )

def generate_digest(filename):

    with open(filename, "rb") as stream:
        contents = stream.read()

    return ScraperContext(
        filename,
        hex(crc32(contents))[2:],
        md5(contents).hexdigest(),
        sha1(contents).hexdigest()
    )
