from __future__ import absolute_import, unicode_literals

from .abstract import Thenable
from .promises import promise

__all__ = [
    'maybe_promise', 'ensure_promise',
    'ppartial', 'preplace', 'ready_promise',
    'starpromise', 'transform', 'wrap',
]


def maybe_promise(p):
    if p:
        if not isinstance(p, Thenable):
            return promise(p)
    return p


def ensure_promise(p):
    if p is None:
        return promise()
    return maybe_promise(p)


def ppartial(p, *args, **kwargs):
    p = ensure_promise(p)
    if args:
        p.args = args + p.args
    if kwargs:
        p.kwargs.update(kwargs)
    return p


def preplace(p, *args, **kwargs):

    def _replacer(*_, **__):
        return p(*args, **kwargs)
    return promise(_replacer)


def ready_promise(callback=None, *args):
    p = ensure_promise(callback)
    p(*args)
    return p


def starpromise(fun, *args, **kwargs):
    return promise(fun, args, kwargs)


def transform(filter_, callback, *filter_args, **filter_kwargs):
    """Filter final argument to a promise.

    E.g. to coerce callback argument to :class:`int`::

        transform(int, callback)

    or a more complex example extracting something from a dict
    and coercing the value to :class:`float`:

    .. code-block:: python

        def filter_key_value(key, filter_, mapping):
            return filter_(mapping[key])

        def get_page_expires(self, url, callback=None):
            return self.request(
                'GET', url,
                callback=transform(get_key, callback, 'PageExpireValue', int),
            )

    """
    callback = ensure_promise(callback)
    P = promise(_transback, (filter_, callback, filter_args, filter_kwargs))
    P.then(promise(), callback.throw)
    return P


def _transback(filter_, callback, args, kwargs, ret):
    try:
        ret = filter_(*args + (ret,), **kwargs)
    except Exception:
        callback.throw()
    else:
        return callback(ret)


def wrap(p):
    """Wrap promise so that if the promise is called with a promise as
    argument, we attach ourselves to that promise instead."""

    def on_call(*args, **kwargs):
        if len(args) == 1 and isinstance(args[0], promise):
            return args[0].then(p)
        else:
            return p(*args, **kwargs)

    return on_call
