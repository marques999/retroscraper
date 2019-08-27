#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import colorama

from shared.gdf import GdfRegion
from shared.tools import get_files
from shared.platforms import PLATFORMS

from multiprocessing.pool import ThreadPool

from scraper.cache import CacheProvider
from scraper.tools import generate_digest, unmagic
from scraper.screenscraper import SkyscraperProvider
from scraper.thread import ScraperProgress, ScraperResponse

SCRAPERS = {
    SkyscraperProvider.ID: SkyscraperProvider
}

def log_success(filename, scraper, title):

    return "%s -> %s %s(%s)" % (
        filename,
        colorama.Fore.GREEN + title,
        colorama.Fore.MAGENTA,
        scraper
    )

def log_failure(filename, scraper):

    return "%s -> %sN/A %s(%s)" % (
        filename,
        colorama.Fore.RED,
        colorama.Fore.MAGENTA,
        scraper
    )

class Retroscraper(object):

    def __init__(self, platform, scraper):

        self.pool = ThreadPool(6)
        self.progress = ScraperProgress()
        self.cache = CacheProvider(platform)
        self.scrapers = [self.cache]
        self.extensions = PLATFORMS.get(platform, {}).get("extensions")

        if scraper in SCRAPERS:

            self.scrapers.append(SCRAPERS[scraper](
                PLATFORMS.get(platform, {}),
                "marques999",
                unmagic("218,176,161,212,167,149,212,164,253,174")
            ))

    def from_path(self, path):

        missingdb = []
        roms = get_files(path, self.extensions)
        context = list(map(generate_digest, roms))
        results = self.pool.map(self.__scrape_rom, context)

        for index, response in enumerate(results):

            if response.found == False:
                missingdb.append(response.filename)
            elif response.cached == False:
                self.cache.set_game(context[index], response)

        if missingdb:
            print(f"\n{colorama.Fore.YELLOW}[!] THE FOLLOWING GAMES WERE NOT FOUND IN THE DATABASE [!]{colorama.Fore.WHITE}")
            print("\n".join(missingdb))

        self.cache.write_gdf()

    def __scrape_rom(self, context):

        filename = os.path.basename(context.filename)
        scraper, result = self.__scrape_game(context)

        if result.found:
            title = result.metadata["title"][GdfRegion.DEFAULT].upper()
            self.progress.success(log_success(filename, scraper, title))
        else:
            self.progress.failure(log_failure(filename, scraper))

        return result

    def __scrape_game(self, context):

        for scraper in self.scrapers:

            response = scraper.get_game(context)

            if response.found:
                return (scraper.ID, response)

        return ("none", ScraperResponse(context.filename, {}, False, False))

if __name__ == "__main__":
    colorama.init()
    rs = Retroscraper("virtualboy", "screenscraper")
    rs.from_path("C:\\Users\\xmarq\\RetroPie\\roms\\virtualboy")
