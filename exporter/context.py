# -*- coding: utf-8 -*-

from pathlib import Path, PurePath

class ExporterContext(object):

    __slots__ = ("media_directory", "roms_directory", "output_directory")

    def __init__(self, platform, **kwargs):

        self.platform = platform
        self.roms_directory = kwargs.get(
            "roms_directory") or Path.home() / "RetroPie"
        self.media_directory = kwargs.get(
            "media_directory") or Path.home() / ".skyscraper" / "cache"
        self.output_directory = kwargs.get(
            "output_directory" or PurePath("D:\\"))
        self.relative = False
