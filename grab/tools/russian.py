# coding: utf-8
from __future__ import absolute_import

from ..tools.encoding import smart_unicode
from pytils.translit import translify
import re

class InvalidMonthName(Exception):
    pass


RE_NOT_ENCHAR = re.compile(u'[^-a-zA-Z0-9]', re.U)
RE_NOT_ENRUCHAR = re.compile(u'[^-a-zA-Zа-яА-ЯёЁ0-9]', re.U)
RE_RUSSIAN_CHAR = re.compile(u'[а-яА-ЯёЁ]', re.U)
RE_DASH = re.compile(r'-+')

def slugify(value, limit=None, default='', lower=True):
    value = smart_unicode(value)

    # Replace all non russian/english chars with "-" char
    # to help pytils not to crash
    value = RE_NOT_ENRUCHAR.sub('-', value)

    # Do transliteration
    value = translify(value)

    # Replace trash with safe "-" char
    value = RE_NOT_ENCHAR.sub('-', value).strip('-')
    if lower:
        value = value.lower()

    # Replace sequences of dashes
    value = RE_DASH.sub('-', value)

    if limit is not None:
        value = value[:limit]

    if value != "":
        return value
    else:
        return default

def parse_ru_month(val):
    names = (None, u'января', u'февраля', u'марта', u'апреля',
             u'мая', u'июня', u'июля', u'августа',
             u'сентября', u'октября', u'ноября', u'декабря')
    names2 = (None, u'январь', u'февраль', u'март', u'апрель',
             u'май', u'июнь', u'июль', u'август',
             u'сентябрь', u'октябрь', u'ноябрь', u'декабрь')
    try:
        return names.index(val.lower())
    except ValueError:
        try:
            return names2.index(val.lower())
        except ValueError:
            raise InvalidMonthName(u'Invalid month name: %s' % val)
