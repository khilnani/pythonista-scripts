from __future__ import absolute_import, unicode_literals

from vine.promises import promise
from vine.synchronization import barrier

from .case import Case, Mock


class test_barrier(Case):

    def setup(self):
        self.m1, self.m2, self.m3 = Mock(), Mock(), Mock()
        self.ps = [promise(self.m1), promise(self.m2), promise(self.m3)]

    def test_evaluate(self):
        x = barrier(self.ps)
        x()
        self.assertFalse(x.ready)
        x()
        self.assertFalse(x.ready)
        x.add(promise())
        x()
        self.assertFalse(x.ready)
        x()
        self.assertTrue(x.ready)
        x()
        x()

        with self.assertRaises(ValueError):
            x.add(promise())

    def test_reverse(self):
        callback = Mock()
        x = barrier(self.ps, callback=promise(callback))
        for p in self.ps:
            p()
        self.assertTrue(x.ready)
        callback.assert_called_with()

    def test_cancel(self):
        x = barrier(self.ps)
        x.cancel()
        for p in self.ps:
            p()
        x.add(promise())
        x.throw(KeyError())
        self.assertFalse(x.ready)

    def test_throw(self):
        x = barrier(self.ps)
        with self.assertRaises(KeyError):
            x.throw(KeyError(10))
