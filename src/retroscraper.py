import os
import msgpack
import colorama
import requests
import threading

from zlib import crc32
from hashlib import md5, sha1
from pathlib import PurePosixPath
from multiprocessing.pool import ThreadPool

from platforms import PLATFORMS
from pegasus import PegasusExporter
from pipeline import localize_metadata, parse_metadata

class ThreadProgress(object):

    def __init__(self):
        self._total = 0
        self._success = 0
        self._failure = 0
        self._lock = threading.Lock()

    def __format_progress(self, message):

        return "%s[%d/%d/%d]%s %s" % (
            colorama.Fore.BLUE,
            self._success,
            self._failure,
            self._total,
            colorama.Style.RESET_ALL,
            message
        )

    def success(self, message):

        with self._lock:
            self._total += 1
            self._success += 1
            print(self.__format_progress(message))

    def failure(self, message):

        with self._lock:
            self._total += 1
            self._failure += 1
            print(self.__format_progress(message))

colorama.init()

def unmagic(contents):

    secret = bytearray("널향한설레임을오늘부터우리는꿈꾸며기도하는오늘부터우리는", "utf-8")

    return "".join(
        chr(int(lhs) ^ rhs)
        for (lhs, rhs) in zip(contents.split(","), secret)
    )

class ThreadContext(object):

  __slots__ = ("filename", "crc32", "md5", "sha1")

  def __init__(self, filename, crc32, md5, sha1):
    self.filename = filename
    self.crc32 = crc32
    self.md5 = md5
    self.sha1 = sha1

class ThreadResult(object):

    __slots__ = ("filename", "metadata", "found", "cached")

    def __init__(self, filename, metadata, found, cached):
        self.filename = filename
        self.metadata = metadata
        self.found = found
        self.cached = cached

class Screenscraper(object):

    def __init__(self, platform, rom_directory):

        self.database = {}
        self.platform = platform
        self.progress = ThreadProgress()
        self.rom_directory = rom_directory
        self.pool = ThreadPool(processes=6)
        self.gdfpath = os.path.abspath(f"{self.platform}.gdf")
        self.extensions = PLATFORMS[self.platform]["extensions"]

        self.authentication = {
            "devid": "muldjord",
            "devpassword": unmagic("158,211,229,216,192,247,142,172,205,168,210,233,187,208,204,212"),
            "ssid": "marques999",
            "sspassword": unmagic("218,176,161,212,167,149,212,164,253,174"),
            "systemeid": PLATFORMS.get(self.platform).get("id").get("screenscraper"),
        }

        self.filenames = (
            os.path.join(root, filename)
            for root, _, filenames in os.walk(self.rom_directory)
            for filename in filenames
            if os.path.splitext(filename)[-1] in self.extensions
        )

        if os.path.exists(self.gdfpath):
            stream = open(self.gdfpath, "rb")
            self.database = msgpack.unpack(stream, encoding="utf-8")
            stream.close()

    def get_context(self, filename):

        with open(filename, "rb") as stream:

            contents = stream.read()

            return ThreadContext(
                filename,
                hex(crc32(contents))[2:],
                md5(contents).hexdigest(),
                sha1(contents).hexdigest()
            )

    def get_media_url(self, media, game):

        query = {
            **self.authentication,
            "jeuid": game["id"]
        }

        if "region" in media and media["region"] != "ss":
            query["media"] = media["type"] + "(" + media["region"] + ")"
        else:
            query["media"] = media["type"]

        return requests.Request(
            method="GET",
            url="https://www.screenscraper.fr/api2/mediaJeu.php",
            params=query
        ).prepare()

    def fetch_screenscraper(self):

        missingdb = []
        context = list(map(self.get_context, self.filenames))
        results = self.pool.map(self.__get_information, context)

        for index, result in enumerate(results):

            if result.found == False:
                missingdb.append(result.filename)
            elif result.cached == False:
                self.database[context[index].sha1] = result.metadata

        if missingdb:
            print(
                f"\n{colorama.Fore.YELLOW}[!] THE FOLLOWING GAMES WERE NOT FOUND IN THE DATABASE [!]{colorama.Fore.WHITE}")
            print("\n".join(missingdb))

        with open(self.gdfpath, "wb") as stream:
            msgpack.pack(self.database, stream, encoding="utf-8")

    def __get_information(self, context):

        if context.sha1 in self.database:
            return self.__from_cache(context)
        else:
            return self.__from_screenscraper(context)

    def __from_cache(self, context):

        filename = os.path.basename(context.filename)
        metadata = self.database[context.sha1]
        title = metadata["title"]["ss"].upper()
        self.progress.success(self.__log_success(filename, title, "cache"))

        return ThreadResult(context.filename, metadata, True, True)

    def __from_screenscraper(self, context):

        response = requests.get("https://www.screenscraper.fr/api2/jeuInfos.php", params={
            **self.authentication,
            "output": "json",
            "sha1": context.sha1,
            "md5": context.md5,
            "crc32": context.crc32
        })

        filename = os.path.basename(context.filename)

        if response.status_code == 200:
            metadata = parse_metadata(response.json()["response"]["jeu"])
            title = metadata["title"]["ss"].upper()
            self.progress.success(self.__log_success(filename, title, "screenscraper"))
            return ThreadResult(context.filename, metadata, True, False)
        else:
            self.progress.failure(self.__log_failure(filename, "screenscraper"))
            return ThreadResult(context.filename, None, False, False)

    @staticmethod
    def __log_success(filename, title, source):
        return f"{filename} -> {colorama.Fore.GREEN}{title} {colorama.Fore.MAGENTA}({source})"

    @staticmethod
    def __log_failure(filename, source):
        return f"{filename} -> {colorama.Fore.RED}N/A {colorama.Fore.MAGENTA}({source})"


Screenscraper("mo5", "D:\\MAME\\software\\to7_cass\\[[WIP]]").fetch_screenscraper()

def test_json():

    import json

    response = requests.get("https://www.screenscraper.fr/api2/jeuInfos.php", params={
        "devid": "muldjord",
        "devpassword": unmagic("158,211,229,216,192,247,142,172,205,168,210,233,187,208,204,212"),
        "ssid": "marques999",
        "sspassword": unmagic("218,176,161,212,167,149,212,164,253,174"),
        "systemeid": "31",
        "output": "json",
        "md5": "f677b6d9475fca8a07b66068ead12c24"
    }).json()

    metadata = parse_metadata(response["response"]["jeu"])
    metadata["checksum"] = "f677b6d9475fca8a07b66068ead12c2"

    with open("screenscraper.json", "w") as stream:
        json.dump(metadata, stream, indent=2)

    localize_metadata(metadata, "en", "us")
    exporter = PegasusExporter(PurePosixPath("/home/pi/RetroPie/roms/atari5200"))
    print(exporter.generate_pegasus([metadata, metadata]))

#test_json()
