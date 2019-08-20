import os
import re
import gzip

from hashlib import sha1
from zipfile import ZipFile
from datetime import datetime
from platforms import ROM_EXTENSIONS
from xml.dom import minidom
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

def get_files(directory, extensions):

    return (
        os.path.join(root, filename)
        for root, _, filenames in os.walk(directory)
        for filename in filenames
        if os.path.splitext(filename)[-1].lower() in extensions
    )

def get_roms(roms_directory, extensions):

    roms = {}

    for root, _, filenames in os.walk(roms_directory):

        for filename in filenames:

            path = os.path.join(root, filename)
            extension = os.path.splitext(filename)[-1].lower()

            if extension in extensions:
                roms[digest_file(path)] = path
            elif extension == ".zip":
                roms[digest_zip(path)], roms[digest_file(path)] = path, path
            elif extension == ".gz":
                roms[digest_gzip(path)], roms[digest_file(path)] = path, path

    return roms
