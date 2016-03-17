import json
import os

from eingefuhrt.parser import get_imports
from eingefuhrt.parser import parse_file

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), 'samples')


def get_extension(filename):
    _base, _sep, ext = filename.partition(os.extsep)
    return ext


def sample_list():
    return (
        os.path.join(SAMPLE_DIR, filename)
        for filename in os.listdir(SAMPLE_DIR)
        if get_extension(filename).lower() == 'py'
    )


def get_metadata(filename):
    name, _ext = os.path.splitext(filename)
    fname_metadata = '{}.json'.format(name)
    with open(fname_metadata) as fp:
        metadata = fp.read()
    return json.loads(metadata)


def get_imports_from_metadata(metadata):
    return (
        imp
        for import_list in metadata.values()
        for imp in import_list
    )


def test_get_imports():
    for filename in sample_list():
        tree = parse_file(filename)

        import_list = list(get_imports(tree))
        expected = list(get_imports_from_metadata(get_metadata(filename)))

        assert len(import_list) == len(expected)

        for imp, exp in zip(import_list, expected):
            assert imp.name == exp['name']
            assert imp.path == exp['path']
