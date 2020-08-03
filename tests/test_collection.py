from src.collection import Collection


def test_smoke():
    assert Collection([]).items == []


def test_all():
    expected = Collection([1, 2, 3])
    collection = Collection([1, 2, 3])
    print(collection.all() == expected)


def test_avg():
    expected = 3
    assert Collection([1, 5]).avg() == expected


def test_chunk():
    expected = Collection([[1, 2], [3, 4]])
    assert Collection([1, 2, 3, 4]).chunk(2) == expected


def test_intersect():
    expected = Collection([1, 2])
    assert Collection([1, 2, 3, 4]).intersect([1, 2]) == expected


def test_is_empty():
    assert Collection([]).is_empty()


def test_is_not_empty():
    assert Collection([1]).is_not_empty()


def test_key_by():
    expected = Collection([{'a': ['a', 'b']}, {'a': ['a', 'c']}])
    sut = Collection([['a', 'b'], ['a', 'c']]).key_by('a')
    assert sut == expected


def test_keys():
    expected = Collection(['a', 'b'])
    sut = Collection({'a': 1, 'b': 2}).keys()
    assert sut == expected


def test_last_none():
    assert Collection([]).last() == None


def test_last_no_arguments():
    expected = 1
    assert Collection([3, 2, 1]).last() == expected


def test_last_function():
    expected = 1
    assert Collection([3, 2, 1]).last(lambda x: x > 0) == expected


def test_map():
    expected = Collection([3, 6, 9])
    assert Collection([1, 2, 3]).map(lambda x: x * 3) == expected


class DummyClass:
    def __init__(self, arg):
        self.arg = arg


def test_map_into():
    expected = Collection([DummyClass(1)])
    assert type(Collection(1).map_into(DummyClass)[0]) == type(expected)


def test_map_spread():
    expected = Collection([1, 5])
    sut = Collection([0, 1, 2, 3]).chunk(2).map_spread(lambda x, y: x + y)
    assert sut == expected


def test_max_value():
    expected = 3
    sut = Collection([1, 2, 3]).max()
    assert sut == expected


def test_max_key():
    expected = 3
    sut = Collection([{'a': 1}, {'a': 3}]).max(field='a')
    assert sut == expected


def test_merge():
    expected = Collection([1, 2, 3, 4])
    sut = Collection([1, 2]).merge(Collection([3, 4]))
    assert expected == sut


def test_nth():
    expected = Collection(['a', 'c'])
    sut = Collection(['a', 'b', 'c']).nth(2)
    assert sut == expected


def test_nth_offset():
    expected = Collection(['b', 'd'])
    sut = Collection(['a', 'b', 'c', 'd']).nth(2, offset=1)
    assert sut == expected


def test_pad():
    expected = Collection([1, 2, 3, 0])
    sut = Collection([1, 2, 3]).pad(4)
    assert sut == expected


def test_pad_left_pad_char():
    expected = Collection(['x', 1, 2, 3])
    sut = Collection([1, 2, 3]).pad(4, left=True, pad_char='x')
    assert sut == expected
