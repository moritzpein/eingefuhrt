import ast
from textwrap import dedent

from eingefuhrt.formatters import hacking
from eingefuhrt.parser import get_imports


def format(code, formatter):
    return formatter(get_imports(ast.parse(code, filename='<test>')))


def test_hacking():
    bad_code = dedent("""\
        from __future__ import absolute_import

        import functools
        from collections import namedtuple

        from mymodule.submodule import a as b, foo, bar, baz
        from .curry import wurst""")

    expected = dedent("""\
        from __future__ import absolute_import

        from collections import namedtuple
        import functools

        from .curry import wurst
        import mymodule.submodule.a as b
        from mymodule.submodule import bar
        from mymodule.submodule import baz
        from mymodule.submodule import foo
        """)

    assert format(bad_code, formatter=hacking) == expected
