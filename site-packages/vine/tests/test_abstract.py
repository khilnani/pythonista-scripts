from __future__ import absolute_import, unicode_literals

from vine.abstract import Thenable
from vine.promises import promise

from .case import Case


class CanThen(object):

    def then(self, x, y):
        pass


class CannotThen(object):
    pass


class test_Thenable(Case):

    def test_isa(self):
        self.assertIsInstance(CanThen(), Thenable)
        self.assertNotIsInstance(CannotThen(), Thenable)

    def test_promise(self):
        self.assertIsInstance(promise(lambda x: x), Thenable)
