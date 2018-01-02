from grouping_decorator import (
    enable, disable,
    GROUP_PUBLIC_API as public
)

def create(group):
    def outer_func(func):
        def _wrap(*args, **kwargs):
            return 'outer({})'.format(*args)
        return _wrap

    @group(outer_func, public)
    def inner_public(val):
        return 'inner_public({})'.format(val)

    @group(outer_func)
    def inner_internal(val):
        return 'inner_internal({})'.format(val)

    @group(outer_func, 'third')
    def inner_third(val):
        return 'inner_third({})'.format(val)

    return inner_public, inner_internal, inner_third
