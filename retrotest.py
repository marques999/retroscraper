from pathlib import PurePath
from scraper.cache import CacheProvider
from scraper.skyscraper import SkyscraperProvider

sha1 = "c7204ba5cfe7d26394b5e22badc580c8ed8c0b37"
skyscraper_directory = PurePath("C:\\Users\\xmarq\\.skyscraper\\cache")

print(SkyscraperProvider("virtualboy", skyscraper_directory).database[sha1])
print(CacheProvider("virtualboy").database[sha1])
