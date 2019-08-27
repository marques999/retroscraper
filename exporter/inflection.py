# -*- coding: utf-8 -*-

import re
import unicodedata

PLURALS = [
    (r"(?i)(quiz)$", r'\1zes'),
    (r"(?i)^(oxen)$", r'\1'),
    (r"(?i)^(ox)$", r'\1en'),
    (r"(?i)(m|l)ice$", r'\1ice'),
    (r"(?i)(m|l)ouse$", r'\1ice'),
    (r"(?i)(matr|vert|ind)(?:ix|ex)$", r'\1ices'),
    (r"(?i)(x|ch|ss|sh)$", r'\1es'),
    (r"(?i)([^aeiouy]|qu)y$", r'\1ies'),
    (r"(?i)(hive)$", r'\1s'),
    (r"(?i)([lr])f$", r'\1ves'),
    (r"(?i)([^f])fe$", r'\1ves'),
    (r"(?i)sis$", 'ses'),
    (r"(?i)([ti])a$", r'\1a'),
    (r"(?i)([ti])um$", r'\1a'),
    (r"(?i)(buffal|potat|tomat)o$", r'\1oes'),
    (r"(?i)(bu)s$", r'\1ses'),
    (r"(?i)(alias|status)$", r'\1es'),
    (r"(?i)(octop|vir)i$", r'\1i'),
    (r"(?i)(octop|vir)us$", r'\1i'),
    (r"(?i)^(ax|test)is$", r'\1es'),
    (r"(?i)s$", 's'),
    (r"$", 's'),
]

SINGULARS = [
    (r"(?i)(database)s$", r'\1'),
    (r"(?i)(quiz)zes$", r'\1'),
    (r"(?i)(matr)ices$", r'\1ix'),
    (r"(?i)(vert|ind)ices$", r'\1ex'),
    (r"(?i)^(ox)en", r'\1'),
    (r"(?i)(alias|status)(es)?$", r'\1'),
    (r"(?i)(octop|vir)(us|i)$", r'\1us'),
    (r"(?i)^(a)x[ie]s$", r'\1xis'),
    (r"(?i)(cris|test)(is|es)$", r'\1is'),
    (r"(?i)(shoe)s$", r'\1'),
    (r"(?i)(o)es$", r'\1'),
    (r"(?i)(bus)(es)?$", r'\1'),
    (r"(?i)(m|l)ice$", r'\1ouse'),
    (r"(?i)(x|ch|ss|sh)es$", r'\1'),
    (r"(?i)(m)ovies$", r'\1ovie'),
    (r"(?i)(s)eries$", r'\1eries'),
    (r"(?i)([^aeiouy]|qu)ies$", r'\1y'),
    (r"(?i)([lr])ves$", r'\1f'),
    (r"(?i)(tive)s$", r'\1'),
    (r"(?i)(hive)s$", r'\1'),
    (r"(?i)([^f])ves$", r'\1fe'),
    (r"(?i)(t)he(sis|ses)$", r"\1hesis"),
    (r"(?i)(s)ynop(sis|ses)$", r"\1ynopsis"),
    (r"(?i)(p)rogno(sis|ses)$", r"\1rognosis"),
    (r"(?i)(p)arenthe(sis|ses)$", r"\1arenthesis"),
    (r"(?i)(d)iagno(sis|ses)$", r"\1iagnosis"),
    (r"(?i)(b)a(sis|ses)$", r"\1asis"),
    (r"(?i)(a)naly(sis|ses)$", r"\1nalysis"),
    (r"(?i)([ti])a$", r'\1um'),
    (r"(?i)(n)ews$", r'\1ews'),
    (r"(?i)(ss)$", r'\1'),
    (r"(?i)s$", ''),
]

UNCOUNTABLES = {
    'equipment',
    'fish',
    'information',
    'jeans',
    'money',
    'rice',
    'series',
    'sheep',
    'species'
}

def camelize(string, uppercase=True):

    if uppercase:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]

def humanize(word):

    word = re.sub(r"_id$", "", word)
    word = word.replace('_', ' ')
    word = re.sub(r"(?i)([a-z\d]*)", lambda m: m.group(1).lower(), word)

    return re.sub(r"^\w", lambda m: m.group(0).upper(), word)

def parameterize(string, separator='-'):

    string = re.sub(r"(?i)[^a-z0-9\-_]+", separator, transliterate(string))

    if separator:
        re_sep = re.escape(separator)
        string = re.sub(r'%s{2,}' % re_sep, separator, string)
        string = re.sub(r"(?i)^{sep}|{sep}$".format(sep=re_sep), '', string)

    return string.lower()

def pluralize(word):

    if not word or word.lower() in UNCOUNTABLES:
        return word

    for rule, replacement in PLURALS:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)

    return word

def singularize(word):

    for inflection in UNCOUNTABLES:
        if re.search(r'(?i)\b(%s)\Z' % inflection, word):
            return word

    for rule, replacement in SINGULARS:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)

    return word

def titleize(word):

    return re.sub(
        r"\b('?[a-z])",
        lambda match: match.group(1).capitalize(),
        humanize(underscore(word))
    )

def transliterate(string):

    return unicodedata.normalize("NFKD", string) \
        .encode("ascii", "ignore") \
        .decode("ascii")

def underscore(word):

    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)

    return re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word) \
        .replace("-", "_") \
        .lower()
