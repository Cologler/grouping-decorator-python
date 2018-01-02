#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools
from collections import defaultdict

# default group use `int`, user group should use `str`
GROUP_INTERNAL_API = 0
GROUP_PUBLIC_API = 1

class _Env:
    def __init__(self):
        self._gdata = {} # global data
        self._mdata = defaultdict(dict) # module data
        self._def_by_module = {}

    def check(self, *, module, group_name):
        if '.' in module:
            module = module.split('.')[0]

        ret = self._mdata[module].get(group_name)
        if ret is None:
            ret = self._gdata.get(group_name)
        if ret is None:
            ret = self._def_by_module.get(module)
        return ret

    def enable(self, group_name, *, module: str=None):
        d = self._gdata if module is None else self._mdata[module]
        d[group_name] = True

    def disable(self, group_name, *, module: str=None):
        d = self._gdata if module is None else self._mdata[module]
        d[group_name] = False

    def default(self, module: str, value: bool):
        ''' set default action for module. '''
        self._def_by_module[module] = value

    def reset(self):
        self._gdata.clear()
        self._mdata.clear()
        self._def_by_module.clear()

        # use default configuration.
        self.default('__main__', True)
        self.enable(GROUP_PUBLIC_API)


_ENV = _Env()
# pylint: disable=C0103
enable = _ENV.enable
disable = _ENV.disable
default = _ENV.default
reset = _ENV.reset
# pylint: enable=C0103
reset()


def runtime_group(decorator, group_name: str=None):
    '''
    if `group_name` is None, use `GROUP_INTERNAL_API` instead.
    '''
    if group_name is None:
        group_name = GROUP_INTERNAL_API

    def _wrap(func):
        decorated_func = decorator(func)
        def grouped_func(*args, **kwargs):
            if _ENV.check(module=func.__module__, group_name=group_name):
                return decorated_func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return functools.update_wrapper(grouped_func, func)

    return _wrap


def compile_group(decorator, group_name: str=None):
    '''
    if `group_name` is None, use `GROUP_INTERNAL_API` instead.
    '''
    if group_name is None:
        group_name = GROUP_INTERNAL_API

    def _wrap(func):
        if _ENV.check(module=func.__module__, group_name=group_name):
            return decorator(func)
        else:
            return func

    return _wrap

# pylint: disable=C0103
group = runtime_group
