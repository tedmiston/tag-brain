from unittest.mock import mock_open, patch

from nose2.tools.params import params

from app import de_dupe, de_hash, load_input


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
    ('#foo #bar baz bar', None, ['#foo', '#bar', 'baz', 'bar']),
)
def test_load_input(input_file_contents, caption, tags_out):
    m = mock_open(read_data=input_file_contents)
    with patch('builtins.open', m):
        assert load_input('_.txt') == (caption, tags_out)
