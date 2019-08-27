# -*- coding: utf-8 -*-

from os import getcwd
from pathlib import PurePath
from itertools import takewhile

class PegasusProvider(object):

    ID = "pegasus"

    def __init__(self, platform, directory=getcwd()):

        self.platform = platform
        self.path = PurePath(directory)
        self.database = self.__read_pegasus()

    def __read_pegasus(self):

        gamedb = {}
        metadata_filename = (self.path / "metadata.pegasus.txt")

        with open(metadata_filename, mode="r", encoding="utf-8") as stream:

            contents = stream.read().split("\n\n\n")
            entries = iter(contents[0].split("\n"))
            mapping = {}

            while entries:
                key, _, value = next(entries, "").partition(": ")

                if key == "description":
                    print(list(takewhile(lambda x: x.startswith("  "), entries)))
                else:
                    mapping[key] = value

            print(mapping)

        return gamedb
