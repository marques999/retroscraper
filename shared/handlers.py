# -*- coding: utf-8 -*-

from datetime import datetime

def string(context, value):
    return value

def integer(context, value):
    return int(value)

def timestamp(formatter):
    return lambda _, value: datetime.fromtimestamp(value).strftime(formatter)
