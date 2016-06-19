from __future__ import absolute_import, unicode_literals

from vine.abstract import Thenable
from vine.funtools import (
    maybe_promise, ppartial, preplace,
    ready_promise, starpromise, transform, wrap,
)
from vine.promises import promise

from .case import Case, Mock


class test_wrap(Case):

    def test_wrap(self):
        cb1 = Mock()
        cb2 = Mock()
        x = wrap(promise(cb1))
        x(1, y=2)
        cb1.assert_called_with(1, y=2)
        p2 = promise(cb2)
        x(p2)
        p2()
        cb1.assert_called_with(cb2())


class test_transform(Case):

    def test_transform(self):
        callback = Mock()

        def filter_key_value(key, filter_, mapping):
            return filter_(mapping[key])

        x = transform(filter_key_value, promise(callback), 'Value', int)
        x({'Value': 303})
        callback.assert_called_with(303)

        with self.assertRaises(KeyError):
            x({})


class test_maybe_promise(Case):

    def test_when_none(self):
        self.assertIsNone(maybe_promise(None))

    def test_when_promise(self):
        p = promise()
        self.assertIs(maybe_promise(p), p)

    def test_when_other(self):
        m = Mock()
        p = maybe_promise(m)
        self.assertIsInstance(p, Thenable)


class test_starpromise(Case):

    def test_apply(self):
        m = Mock()
        p = starpromise(m, 1, 2, z=3)
        p()
        m.assert_called_with(1, 2, z=3)


class test_ready_promise(Case):

    def test_apply(self):
        m = Mock()
        p = ready_promise(m, 1, 2, 3)
        m.assert_called_with(1, 2, 3)
        self.assertTrue(p.ready)


class test_ppartial(Case):

    def test_apply(self):
        m = Mock()
        p = ppartial(m, 1)
        p()
        m.assert_called_with(1)
        p = ppartial(m, z=2)
        p()
        m.assert_called_with(z=2)


class test_preplace(Case):

    def test_preplace(self):
        m = Mock()
        p = promise(m)
        p2 = preplace(p, 1, 2, z=3)
        p2(4, 5, x=3)
        m.assert_called_with(1, 2, z=3)
