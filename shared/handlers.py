# -*- coding: utf-8 -*-

from datetime import datetime

def string(context, value):
    return value

def timestamp(format):
    return lambda _, value: datetime.fromtimestamp(value).strftime("%Y-%m-%d")
