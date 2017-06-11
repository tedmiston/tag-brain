from unittest.mock import mock_open, patch

from nose2.tools.params import params

from app import build_header, create_tag_str, de_dupe, de_hash, get_collapser, load_input


def check_equalish(list1, list2):
    """Number of elements and content must be the same but not order."""
    return len(list1) == len(list2) and sorted(list1) == sorted(list2)


@params(
    ([], []),
    (['a'], ['a']),
    (['a', 'a'], ['a']),
    (['a', 'a', 'a'], ['a']),
    (['a', 'b', 'a', 'c', 'b'], ['a', 'b', 'c']),
)
def test_de_dupe(tags_in, tags_out):
    assert check_equalish(de_dupe(tags_in), tags_out)


@params(
    ([], []),
    (['#a'], ['a']),
    (['a', 'b'], ['a', 'b']),
    (['#a', 'b'], ['a', 'b']),
    (['#a', '#b'], ['a', 'b']),
)
def test_de_hash(tags_in, tags_out):
    assert check_equalish(de_hash(tags_in), tags_out)


@params(
    ('', None, []),
    ('foo', None, ['foo']),
    ('#foo #bar', None, ['#foo', '#bar']),
    ('#foo  #bar', None, ['#foo', '#bar']),
    ('#foo #bar baz bar', None, ['#foo', '#bar', 'baz', 'bar']),
    ('Sample caption\n---', 'Sample caption', []),
    ('Sample caption\n---\n', 'Sample caption', []),
    ('Sample caption\n---\nfoo bar', 'Sample caption', ['foo', 'bar']),
    ('Sample caption\n---\n#foo #bar', 'Sample caption', ['#foo', '#bar']),
    ('Sample caption\n\n---\n\n#foo #bar', 'Sample caption', ['#foo', '#bar']),
    ('Sample\n\nmulti-line\n\ncaption\n\n---\n\n#foo #bar', 'Sample\n\nmulti-line\n\ncaption', ['#foo', '#bar']),
)
def test_load_input(input_file_contents, caption, tags_out):
    m = mock_open(read_data=input_file_contents)
    with patch('builtins.open', m):
        assert load_input('_.txt') == (caption, tags_out)


@params(
    ([], '0 tags'),
    (['a'], '1 tags'),
    (list('ab'), '2 tags'),
    (list('abc'), '3 tags'),
    (list('abcdefghijklmnopqrstuvwxyz012'), '29 tags'),
    (list('abcdefghijklmnopqrstuvwxyz0123'), '30 tags'),
    (list('abcdefghijklmnopqrstuvwxyz01234'), '31 tags *Warning: You have exceeded the max of 30 tags*'),
)
def test_build_header(tags, expected):
    assert build_header(tags=tags) == expected


@params(
    (True, '\n.\n.\n.\n.\n.'),
    (False, ''),
)
def test_get_collapser(show, expected):
    assert get_collapser(show=show) == expected


@params(
    ([], True, ''),
    ([], False, ''),
    (['a'], True, '#a'),
    (['a'], False, '#a'),
    (['a', 'b', 'c'], True, '#a #b #c'),
    (['a', 'b', 'c'], False, '#a\n#b\n#c'),
)
def test_create_tag_str(tags, spaces, expected):
    assert create_tag_str(tags=tags, spaces=spaces) == expected
