# -*- coding: utf-8 -*-

PLATFORMS = {
    "3do": {
        "name": "3DO",
        "manufacturer": "Panasonic",
        "scrapers": {
            "mobygames": 35,
            "screenscraper": 29
        },
        "extensions": {
            ".bin", ".chd", ".cue", ".iso"
        }
    },
    "amiga": {
        "name": "Commodore Amiga",
        "manufacturer": "Commodore",
        "scrapers": {
            "mobygames": 19,
            "screenscraper": 64
        },
        "extensions": {
            ".adf", ".adz", ".dms", ".exe", ".fdi", ".hdf", ".hdz", ".ipf"
        }
    },
    "amstradcpc": {
        "name": "Amstrad CPC",
        "manufacturer": "Amstrad",
        "scrapers": {
            "mobygames": 60,
            "screenscraper": 65
        },
        "extensions": {
            ".cdt", ".dsk"
        }
    },
    "apple2": {
        "name": "Apple II",
        "manufacturer": "Apple",
        "scrapers": {
            "mobygames": 31,
            "screenscraper": 86
        },
        "extensions": {
            ".do", ".dsk", ".nib", ".po"
        }
    },
    "apple2gs": {
        "name": "Apple IIGS",
        "manufacturer": "Apple",
        "scrapers": {
            "screenscraper": 217
        },
        "extensions": {
            ".2mg", ".do", ".po"
        }
    },
    "atari2600": {
        "name": "Atari 2600",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 28,
            "screenscraper": 26
        },
        "extensions": {
            ".a26", ".bin", ".rom"
        }
    },
    "atari5200": {
        "name": " Atari 5200",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 33,
            "screenscraper": 40
        },
        "extensions": {
            ".a52", ".bin"
        }
    },
    "atari7800": {
        "name": "Atari 7800",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 34,
            "screenscraper": 41
        },
        "extensions": {
            ".a78", ".bin"
        }
    },
    "atari800": {
        "name": "Atari 400/800",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 39,
            "screenscraper": 43
        },
        "extensions": {
            ".atr", ".bas", ".bin", ".xex", ".xfd"
        }
    },
    "atarijaguar": {
        "name": "Atari Jaguar",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 17,
            "screenscraper": 27
        },
        "extensions": {
            ".j64", ".jag"
        }
    },
    "atarilynx": {
        "name": "Atari Lynx",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 18,
            "screenscraper": 28
        },
        "extensions": {
            ".lnx"
        }
    },
    "atarist": {
        "name": "Atari ST",
        "manufacturer": "Atari",
        "scrapers": {
            "mobygames": 24,
            "screenscraper": 42
        },
        "extensions": {
            ".ctr", ".img", ".ipf", ".msa", ".raw", ".rom", ".st", ".stx"
        }
    },
    "c64": {
        "name": "Commodore 64",
        "maufacturer": "Commodore",
        "scrapers": {
            "mobygames": 27,
            "screenscraper": 66
        },
        "extensions": {
            ".crt", ".d64", ".g64", ".p00", ".prg" ".t64", ".tap", ".x64"
        }
    },
    "coco": {
        "name": "Color Computer",
        "manufacturer": "Tandy",
        "scrapers": {
            "mobygames": 62,
            "screenscraper": 144
        },
        "extensions": {
            ".asc", ".bas", ".cas", ".ccc", ".dmk", ".dsk", ".jvc", ".os9", ".rom", ".sna", ".vdk", ".wav"
        }
    },
    "coleco": {
        "name": "ColecoVision",
        "manufacturer": "Coleco",
        "scrapers": {
            "mobygames": 29,
            "screenscraper": 75
        },
        "extensions": {
            ".bin", ".col", ".rom"
        }
    },
    "dragon32": {
        "name": "Dragon 32/64",
        "manufacturer": "Dragon",
        "scrapers": {
            "mobygames": 79,
            "screenscraper": 91
        },
        "extensions": {".asc", ".bas", ".cas", ".ccc", ".dmk", ".dsk", ".jvc", ".os9", ".rom", ".sna", ".vdk", ".wav"}
    },
    "dreamcast": {
        "name": "Sega Dreamcast",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 8,
            "screenscraper": 23
        },
        "extensions": {".cdi", ".chd", ".gdi"}
    },
    "fba": {
        "name": "Final Burn Alpha",
        "manufacturer": "Arcade",
        "scrapers": {
            "screenscraper": 75
        },
        "extensions": {".7z", ".zip"}
    },
    "fds": {
        "name": "Famicom Disk System",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 22,
            "screenscraper": 106
        },
        "extensions": {".fds", ".nes", ".qd"}
    },
    "gameandwatch": {
        "name": "Game & Watch",
        "manufacturer": "Nintendo",
        "scrapers": {
            "screenscraper": 52
        },
        "extensions": {".mgw"}
    },
    "gamegear": {
        "name": "Sega Game Gear",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 25,
            "screenscraper": 21
        },
        "extensions": {".bin", ".gg", ".sms"}
    },
    "gb": {
        "name": "Game Boy",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 10,
            "screenscraper": 9
        },
        "extensions": {".gb"}
    },
    "gba": {
        "name": "Game Boy Advance",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 12,
            "screenscraper": 12
        },
        "extensions": {".gba"}
    },
    "gbc": {
        "name": "Game Boy Color",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 11,
            "screenscraper": 10
        },
        "extensions": {".gbc"}
    },
    "gc": {
        "name": "Nintendo GameCube",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 14,
            "screenscraper": 13
        },
        "extrensions": {".gcm", ".gcz", ".iso"}
    },
    "genesis": {
        "name": "Sega Genesis",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 16,
            "screenscraper": 1
        },
        "extensions": {".bin", ".gen", ".md", ".smd"}
    },
    "intellivision": {
        "name": "Intellivision",
        "manufacturer": "Mattel",
        "scrapers": {
            "mobygames": 30,
            "screenscraper": 115
        },
        "extensions": {".bin", ".int", ".rom"}
    },
    "mame": {
        "name": "Multiple Arcade Machine Emulator",
        "manufacturer": "Arcade",
        "scrapers": {
            "screenscraper": 75
        },
        "extensions": {".7z", ".zip"}
    },
    "mastersystem": {
        "name": "Sega Master System",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 26,
            "screenscraper": 2
        },
        "extensions": {".bin", ".sms"}
    },
    "megacd": {
        "name": "Sega Mega CD",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 20,
            "screenscraper": 20
        },
        "extensions": {
            ".bin", ".chd", ".cue", ".iso"
        }
    },
    "megadrive": {
        "name": "Sega Mega Drive",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 16,
            "screenscraper": 1
        },
        "extensions": {
            ".bin", ".gen", ".md", ".smd"
        }
    },
    "mo5": {
        "name": "Thomson MO/TO",
        "description": "Thomson",
        "scrapers": {
            "screenscraper": 141
        },
        "extensions": {
            ".bin", ".fd", ".k7", ".m5", ".qd", ".sap", ".wav"
        }
    },
    "msx": {
        "name": "MSX",
        "manufacturer": "ASCII/Microsoft",
        "scrapers": {
            "mobygames": 57,
            "screenscraper": 113
        },
        "extensions": {
            ".dsk", ".mx1", ".mx2", ".rom"
        }
    },
    "n64": {
        "name": "Nintendo 64",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 9,
            "screenscraper": 14
        },
        "extensions": {
            ".n64", ".v64", ".z64"
        }
    },
    "nds": {
        "name": "Nintendo DS",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 44,
            "screenscraper": 15
        },
        "extensions": {
            ".nds", ".zip"
        }
    },
    "neogeo": {
        "name": "Neo Geo",
        "manufacturer": "SNK",
        "scrapers": {
            "mobygames": 36,
            "screenscraper": 142
        },
        "extensions": {
            ".7z", ".zip"
        }
    },
    "nes": {
        "name": "Nintendo Entertainment System",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 22,
            "screenscraper": 3
        },
        "extensions": {".fds", ".nes"}
    },
    "ngp": {
        "name": "Neo Geo Pocket",
        "manufacturer": "SNK",
        "scrapers": {
            "mobygames": 52,
            "screenscraper": 25
        },
        "extensions": {".ngp"}
    },
    "ngc": {
        "name": "Neo Geo Pocket Color",
        "manufacturer": "SNK",
        "scrapers": {
            "mobygames": 53,
            "screenscraper": 82
        },
        "extensions": {".ngc"}
    },
    "oric": {
        "name": "Oric-1",
        "manufacturer": "Tangerine Computer Systems",
        "scrapers": {
            "mobygames": 111,
            "screenscraper": 131
        },
        "extensions": {".dsk", ".tap"}
    },
    "pc": {
        "name": "PC/AT",
        "manufacturer": "IBM",
        "scrapers": {
            "screenscraper": 135
        },
        "extensions": {
            ".bat", ".com",  ".exe"
        }
    },
    "pc88": {
        "name": "PC-8801/PC-88VA",
        "manufacturer": "NEC",
        "scrapers": {
            "mobygames": 94
        },
        "extensions": {
            ".2d", ".cmt", ".d88", ".t88"
        }
    },
    "pc98": {
        "name": "PC-9801/PC-9821",
        "manufacturer": "NEC",
        "scrapers": {
            "screenscraper": 0
        },
        "extensions": {
            ".d88", ".d98", ".fdi", ".xdf", ".hdm", ".dup", ".2hd", ".tfd", ".hdi", ".thd", ".nhd", ".hdd", ".fdd"
        }
    },
    "pcengine": {
        "name": "PC Engine",
        "manufacturer": "NEC",
        "scrapers": {
            "screenscraper": 31
        },
        "extensions": {
            ".bin", ".ccd", ".chd", ".cue", ".iso", ".pce"
        }
    },
    "pcfx": {
        "name": "PC-FX",
        "manufacturer": "NEC",
        "scrapers": {
            "mobygames": 59,
            "screenscraper": 72
        },
        "extensions": {
            ".bin", ".ccd", ".chd", ".cue", ".img", ".iso"
        }
    },
    "ps2": {
        "name": "PlayStation 2",
        "manufacturer": "Sony",
        "scrapers": {
            "mobygames": 7,
            "screenscraper": 58
        },
        "extensions": {
            ".bin", ".cso", ".ima", ".img", ".iso", ".mdf", ".z"
        }
    },
    "psp": {
        "name": "PlayStation Portable",
        "manufacturer": "Sony",
        "scrapers": {
            "mobygames": 46,
            "screenscraper": 61
        },
        "extensions": {
            ".cso", ".iso", ".pbp"
        }
    },
    "saturn": {
        "name": "Sega Saturn",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 23,
            "screenscraper": 22,
        },
        "extensions": {
            ".bin", ".chd", ".cue", ".iso", ".mdf"
        }
    },
    "sega32x": {
        "name": "Sega 32X",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 21,
            "screenscraper": 19
        },
        "extensions": {
            ".32x", ".bin"
        }
    },
    "segacd": {
        "name": "Sega-CD",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 20,
            "screenscraper": 20
        },
        "extensions": {
            ".bin", ".chd", ".cue", ".iso"
        }
    },
    "sg-1000": {
        "name": "Sega SG-1000",
        "manufacturer": "Sega",
        "scrapers": {
            "mobygames": 114,
            "screenscraper": 109
        },
        "extensions": {
            ".sg"
        }
    },
    "snes": {
        "name": "Super Nintendo Entertainment System",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 15,
            "screenscraper": 4
        },
        "extensions": {
            ".bin", ".bs", ".fig", ".mgd", ".sfc", ".smc", ".swc"
        }
    },
    "ti99": {
        "name": "TI-99/4A",
        "manufacturer": "Texas Instruments",
        "scrapers": {
            "mobygames": 47,
            "screenscraper": 205
        },
        "extensions": {
            ".ctg"
        }
    },
    "trs-80": {
        "name": "Tandy TRS-80",
        "manufacturer": "Tandy",
        "scrapers": {
            "mobygames": 58,
            "screenscraper": 144
        },
        "extensions": {
            ".dsk"
        }
    },
    "vectrex": {
        "name": "Vectrex",
        "manufacturer": "GCE",
        "scrapers": {
            "mobygames": 37,
            "screenscraper": 102
        },
        "extensions": {
            ".bin", ".vec"
        }
    },
    "videopac": {
        "name": "Videopac G7000",
        "manufacturer": "Philips",
        "scrapers": {
            "screenscraper": 104,
            "mobygames": 128
        },
        "extensions": {
            ".bin"
        }
    },
    "virtualboy": {
        "name": "Virtual Boy",
        "manufacturer": "Nintendo",
        "scrapers": {
            "mobygames": 38,
            "screenscraper": 11
        },
        "extensions": {
            ".vb"
        }
    },
    "x1": {
        "name": "Sharp X1",
        "manufacturer": "Sharp",
        "scrapers": {
            "mobygames": 121
        },
        "extensions": {
            ".2d", ".2hd", ".cmd", ".d88", ".dx1", ".dup", ".hdm", ".tfd", ".xdf"
        }
    },
    "x68000": {
        "name": "Sharp X68000",
        "manufacturer": "Sharp",
        "scrapers": {
            "mobygames": 106,
            "screenscraper": 79
        },
        "extensions": {
            ".2hd", ".2hs", ".d88", ".dim", ".dup", ".hdm", ".xdf"
        }
    },
    "wonderswan": {
        "name": "WonderSwan",
        "manufacturer": "Bandai",
        "scrapers": {
            "mobygames": 48,
            "screenscraper": 45
        },
        "extensions": {
            ".ws"
        }
    },
    "wonderswancolor": {
        "name": "WonderSwan Color",
        "manufacturer": "Bandai",
        "scrapers": {
            "mobygames": 49,
            "screenscraper": 46
        },
        "extensions": {
            ".wsc"
        }
    },
    "zx81": {
        "name": "ZX81",
        "manufacturer": "Sinclair",
        "scrapers": {
            "mobygames": 119,
            "screenscraper": 77
        },
        "extensions": {
            ".p", ".tzx", ".t81"
        }
    },
    "zxspectrum": {
        "name": "ZX Spectrum",
        "manufacturer": "Sinclair",
        "scrapers": {
            "screenscraper": 76
        },
        "extensions": {
            ".dsk", ".fdi", ".img", ".mgt", ".scl", ".sna", ".szx", ".tap", ".trd", ".udi", ".tzx", ".z80"
        }
    }
}
