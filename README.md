# grouping-decorator

For example,
I try to use the module [typecheck-decorator](https://github.com/prechelt/typecheck-decorator) to check python arguments types:

``` py
# file: bear/__init__.py
import typecheck as tc

@tc.typecheck
def foo1(a:int, b=None, c:str="mydefault") -> bool:
    pass

@tc.typecheck
def _foo2(a:int, b=None, c:str="mydefault") -> bool:
    pass
```

simple.

but `_foo2` should only use inside the `bear`.
so is possible to do that:

* enable `typecheck` for `_foo2` when doing unittest
* disable `typecheck` for `_foo2` when other `.py` import `bear`

so I use grouping-decorator:

``` py
# file: bear/__init__.py

...
from grouping_decorator import group

@group(tc.typecheck, 'make a group name')
def _foo2(a:int, b=None, c:str="mydefault") -> bool:
    pass
```

now you can `enable` or `disable` it by group name any time.
