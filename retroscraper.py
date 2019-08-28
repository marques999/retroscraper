#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import colorama

from shared.gdf import GdfRegions
from shared.tools import get_files
from shared.platforms import PLATFORMS

from multiprocessing.pool import ThreadPool

from scraper.cache import CacheProvider
from scraper.pegasus import PegasusProvider
from scraper.tools import generate_digest, unmagic
from scraper.skyscraper import SkyscraperProvider
from scraper.screenscraper import ScreenscraperProvider
from scraper.thread import ScraperProgress, ScraperResponse

SCRAPERS = {
    PegasusProvider.ID: PegasusProvider,
    SkyscraperProvider.ID: SkyscraperProvider,
    ScreenscraperProvider.ID: ScreenscraperProvider
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

def get_cpus():

    if "NUMBER_OF_PROCESSORS" in os.environ:
        return int(os.environ["NUMBER_OF_PROCESSORS"])

    if hasattr(os, "sysconf"):

        if "SC_NPROCESSORS_ONLN" not in os.sysconf_names:
            return int(os.popen2("sysctl -n hw.ncpu")[1].read())

        count = os.sysconf["SC_NPROCESSORS_ONLN"]

        if isinstance(count, int) and count > 0:
            return count

    return 1

class Retroscraper(object):

    def __init__(self, platform, scraper):

        self.cache = CacheProvider(platform)
        self.scrapers = [self.cache]
        self.progress = ScraperProgress()
        self.pool = ThreadPool(get_cpus() * 2)
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
            title = result.metadata["title"][GdfRegions.DEFAULT].upper()
            self.progress.success(log_success(filename, scraper, title))
        else:
            self.progress.failure(log_failure(filename, scraper))

        return result

    def __scrape_game(self, context):

        for scraper in self.scrapers:

            response = scraper.get_game(context)

            if response.found:
                return (scraper.ID, response)

        return ("none", ScraperResponse.error(context.filename, "none"))

if __name__ == "__main__":
    colorama.init()
    rs = Retroscraper("virtualboy", "screenscraper")
    rs.from_path("C:\\Users\\xmarq\\RetroPie\\roms\\virtualboy")
