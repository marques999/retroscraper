# -*- coding: utf-8 -*-

from os import path, walk

def export(exporter, context, metadata):

     return dict(
         (destination, exporter(context, metadata[source]))
         for destination, (source, exporter) in exporter.items()
         if source in metadata
     )

def get_files(directory, extensions):

    return (
        path.join(root, filename)
        for root, _, filenames in walk(directory)
        for filename in filenames
        if not extensions or path.splitext(filename)[-1].lower() in extensions
    )
