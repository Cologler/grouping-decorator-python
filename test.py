#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import traceback
import unittest
from grouping_decorator import (
    enable, disable, reset,
    GROUP_PUBLIC_API as public,
    runtime_group, compile_group
)
import test_out as to


def create(group):
    def outer_func(func):
        def _wrap(*args, **kwargs):
            return 'outer({})'.format(*args)
        return _wrap

    # 0: public
    @group(outer_func, public)
    def inner_public(val):
        return 'inner_public({})'.format(val)

    # 1: internal
    @group(outer_func)
    def inner_internal(val):
        return 'inner_internal({})'.format(val)

    # 2: user defined
    @group(outer_func, 'third')
    def inner_third(val):
        return 'inner_third({})'.format(val)

    return inner_public, inner_internal, inner_third


class Test(unittest.TestCase):
    def test_runtime_group(self):
        reset()
        inner_funcs = create(runtime_group)
        outer_funcs = to.create(runtime_group)

        # public always work.
        self.assertEqual(inner_funcs[0]('1'), 'outer(1)')
        self.assertEqual(outer_funcs[0]('1'), 'outer(1)')

        # internal in other module does not work.
        self.assertEqual(inner_funcs[1]('1'), 'outer(1)')
        self.assertEqual(outer_funcs[1]('1'), 'inner_internal(1)')

        # user group default disable
        self.assertEqual(inner_funcs[2]('1'), 'outer(1)')
        self.assertEqual(outer_funcs[2]('1'), 'inner_third(1)')
        enable('third')
        self.assertEqual(outer_funcs[2]('1'), 'outer(1)')

    def test_compile_group(self):
        reset()
        inner_funcs = create(compile_group)
        outer_funcs = to.create(compile_group)

        # public always work.
        self.assertEqual(inner_funcs[0]('1'), 'outer(1)')
        self.assertEqual(outer_funcs[0]('1'), 'outer(1)')

        # internal in other module does not work.
        self.assertEqual(inner_funcs[1]('1'), 'outer(1)')
        self.assertEqual(outer_funcs[1]('1'), 'inner_internal(1)')

        # user group default disable
        self.assertEqual(inner_funcs[2]('1'), 'outer(1)')
        self.assertEqual(outer_funcs[2]('1'), 'inner_third(1)')
        enable('third')
        self.assertEqual(outer_funcs[2]('1'), 'inner_third(1)')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        unittest.main()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    main()
