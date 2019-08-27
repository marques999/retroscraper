# -*- coding: utf-8 -*-

import os
import msgpack

from pathlib import PurePath
from scraper.thread import ScraperResponse

class CacheProvider(object):

    ID = "cache"
    URL = PurePath(os.getcwd()) / "cache"

    def __init__(self, platform, directory=None):

        self.platform = platform
        self.directory = directory or self.URL
        self.gdfpath = (self.directory / platform).with_suffix(".gdf")
        self.database = self.__read_gdf()

    def __read_gdf(self):

        if not os.path.exists(self.gdfpath):
            return {}

        with open(self.gdfpath, "rb") as stream:
            return msgpack.unpack(stream, encoding="utf-8")

    def write_gdf(self):

        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)

        with open(self.gdfpath, "wb") as stream:
            msgpack.pack(self.database, stream, encoding="utf-8")

    def set_game(self, request, response):

        self.database[request.sha1] = response.metadata

    def get_game(self, request):

        resource = self.database.get(request.sha1)

        if resource:
            return ScraperResponse.in_cache(request, resource)

        return ScraperResponse.error(request, self.ID)
