# -*- coding: utf-8 -*-

import colorama
import threading

class ScraperContext(object):

    __slots__ = ("filename", "crc32", "md5", "sha1")

    def __init__(self, filename, crc32, md5, sha1):

        self.md5 = md5
        self.sha1 = sha1
        self.crc32 = crc32
        self.filename = filename

class ScraperResponse(object):

    __slots__ = ("filename", "metadata", "found", "cached")

    def __init__(self, filename, metadata, found, cached):

        self.found = found
        self.cached = cached
        self.filename = filename
        self.metadata = metadata

    @staticmethod
    def error(context, message):
        return ScraperResponse(context.filename, message, False, False)

    @staticmethod
    def in_cache(context, metadata):
        return ScraperResponse(context.filename, metadata, True, True)

    @staticmethod
    def success(context, metadata):
        return ScraperResponse(context.filename, metadata, True, False)

class ScraperProgress(object):

    __slots__ = ("_total", "_success", "_failure", "_lock")

    def __init__(self):

        self._total = 0
        self._failure = 0
        self._success = 0
        self._lock = threading.Lock()

    def success(self, message):

        with self._lock:
            self._total += 1
            self._success += 1
            self.__print(message)

    def failure(self, message):

        with self._lock:
            self._total += 1
            self._failure += 1
            self.__print(message)

    def __print(self, message):

        print("%s[%d/%d/%d]%s %s" % (
            colorama.Fore.BLUE,
            self._success,
            self._failure,
            self._total,
            colorama.Fore.RESET,
            message
        ))
