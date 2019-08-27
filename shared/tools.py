# -*- coding: utf-8 -*-

import os
import re

from datetime import datetime

def merge_dictionaries(*collections):

    result = {}

    for collection in collections:
        result.update(collection.copy())

    return result

def export(exporter, context, metadata):

     return dict(
         (destination, exporter(context, metadata[source]))
         for destination, (source, exporter) in exporter.items()
         if source in metadata
     )

def get_files(directory, extensions):

    return (
        os.path.join(root, filename)
        for root, _, filenames in os.walk(directory)
        for filename in filenames
        if not extensions or os.path.splitext(filename)[-1].lower() in extensions
    )

DATETIME_REGEX = [
    ("%Y", re.compile("^\\d{4}$")),
    ("%Y-%m", re.compile("^\\d{4}-[0-1]{1}\\d{1}$")),
    ("%Y-%m-%d", re.compile("^\\d{4}-[0-1]{1}\\d{1}-[0-3]{1}\\d{1}$")),
    ("%m/%d/%Y", re.compile("^[0-1]{1}\\d{1}/[0-3]{1}\\d{1}/\\d{4}$")),
    ("%Y-%M-%d", re.compile("^\\d{4}-[a-zA-Z]{3}-[0-3]{1}\\d{1}$")),
    ("%M, %Y", re.compile("^[a-zA-z]{3}, \\d{4}$")),
    ("%M %d, %Y", re.compile("^[a-zA-z]{3} ([0-3]{1})?\\d{1}, \\d{4}$"))
]

def parse_datetime(context, timestamp):

    for formatter, regex in DATETIME_REGEX:
        if regex.search(timestamp):
            return int(datetime.strptime(timestamp, formatter).timestamp())

    return datetime.now()
