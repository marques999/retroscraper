from pathlib import PurePath
from scraper.cache import CacheProvider
from scraper.skyscraper import SkyscraperProvider

sha1 = "c7204ba5cfe7d26394b5e22badc580c8ed8c0b37"

print(SkyscraperProvider("virtualboy").database[sha1])
print(CacheProvider("virtualboy").database[sha1])
