from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys
import requests
import pkgutil

# from . import __version__
from ._compat import to_string, to_unicode, string_types


def get_stop_words(language):
    try:
        stopwords_data = pkgutil.get_data("sumy", "data/stopwords/%s.txt" % language)
    except IOError as e:
        raise LookupError("Stop-words are not available for language %s." % language)
    return parse_stop_words(stopwords_data)


def parse_stop_words(data):
    return frozenset(w.rstrip() for w in to_unicode(data).splitlines() if w)
