"""Promises, promises, promises"""
from __future__ import absolute_import, unicode_literals

from collections import namedtuple

from .abstract import Thenable
from .promises import promise
from .synchronization import barrier
from .funtools import (
    maybe_promise, ensure_promise,
    ppartial, preplace, starpromise, transform, wrap,
)

version_info_t = namedtuple(
    'version_info_t', ('major', 'minor', 'micro', 'releaselevel', 'serial'),
)

VERSION = version_info = version_info_t(1, 1, 0, '', '')

__version__ = '{0.major}.{0.minor}.{0.micro}{0.releaselevel}'.format(VERSION)
__author__ = 'Ask Solem'
__contact__ = 'ask@celeryproject.org'
__homepage__ = 'http://github.com/celery/vine',
__docformat__ = 'restructuredtext'

# -eof meta-

__all__ = [
    'Thenable', 'promise', 'barrier',
    'maybe_promise', 'ensure_promise',
    'ppartial', 'preplace', 'starpromise', 'transform', 'wrap',
]
