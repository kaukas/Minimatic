#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from decorator import decorator

fixture_path = os.path.dirname(os.path.abspath(__file__))
global beaker_container
beaker_container = dict()

config = {
    'pylons.paths': {'static_files': fixture_path},
    'debug': False,
}

def beaker_cache(*args, **kwargs):
    beaker_container.update(kwargs)

    @decorator
    def wrapper(f, *a, **kw):
        return f(*a, **kw)

    return wrapper

memo = {}
def memoize(*args, **kwargs):

    @decorator
    def memoizer(f, *a, **kw):
        key = repr(f) + repr(a) + repr(kw)
        if not memo.has_key(key):
            memo[key] = f(*a, **kw)
        return memo[key]

    return memoizer
