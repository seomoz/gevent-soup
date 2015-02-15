# -*- coding: utf-8 -*-
"""Miscellaneous gevent-related things."""

# I m p o r t s

import time
try:
    import gevent
    assert hasattr(gevent, 'sleep')
except ImportError:
    pass

# F u n c t i o n s

# Add a cswitch method which will trigger a voluntary context switch if
# we've been running awhile. For now, we base that solely on wall-clock
# time to keep things simple. Consider adding CPU time to the logic if
# the present logic proves deficient.
class GeventContextMixin(object):
    __SLICE = 1.0

    def cswitch(self):
        now = time.time()
        try:
            then = self.__switched
        except AttributeError:
            self.__switched = then = now
        if now - then >= self.__SLICE:
            gevent.sleep(0)
            self.__switched = time.time()
