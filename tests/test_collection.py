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
    expected = DummyClass(1)
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


def test_partition():
    expected_odd = Collection([1, 3, 5])
    expected_even = Collection([2, 4, 6])
    actual_even, actual_odd = Collection([1, 2, 3, 4, 5, 6]).partition(lambda x: x % 2 == 0)
    assert expected_even == actual_even
    assert expected_odd == actual_odd


def test_pop():
    expected_collection = Collection([1, 2])
    expected_last_item = 3
    sut = Collection([1, 2, 3])
    last_item = sut.pop()
    assert sut == expected_collection
    assert last_item == expected_last_item


def test_prepend():
    expected = Collection([0, 1, 2])
    sut = Collection([1, 2]).prepend(0)
    assert sut == expected


def test_append():
    expected = Collection([1, 2, 3])
    sut = Collection([1, 2]).push(3)
    assert sut == expected


def test_random():
    expected_results = [1, 2]
    sut = Collection([1, 2]).random(1)
    assert sut in expected_results


def test_random_multiple():
    expected_results = [1, 2, 3]
    sut = Collection([1, 2, 3]).random(2)
    assert sut[0] in expected_results
    assert sut[1] in expected_results


def test_reject():
    expected = Collection([1, 2, 3])
    sut = Collection([1, 2, 3, 4, 5, 6]).reject(lambda x: x > 3)
    assert sut == expected


def test_reverse():
    expected = Collection([3, 2, 1])
    sut = Collection([1, 2, 3]).reverse()
    assert sut == expected


def test_search():
    expected = 1
    sut = Collection([1, 2, 3]).search(2)
    assert sut == expected


def test_shift():
    expected = Collection([2, 3])
    sut = Collection([1, 2, 3])
    assert sut.shift() == expected
    assert sut == expected


def test_shuffle():
    expected_result = Collection([1, 2])
    other_expected_result = Collection([2, 1])
    sut = Collection([1, 2]).shuffle()
    assert sut == expected_result or sut == other_expected_result


def test_skip_until():
    expected = Collection([3, 1])
    sut = Collection([2, 1, 1, 1, 2, 3, 1]).skip_until(lambda x: x > 2)
    assert sut == expected


def test_skip_while():
    expected = Collection([3, 5, 1])
    sut = Collection([2, 1, 1, 1, 2, 3, 3, 5, 1]).skip_while(lambda x: x > 2)
    assert sut == expected


def test_slice():
    expected = Collection([2, 3])
    sut = Collection([1, 2, 3, 4]).slice(1, 2)
    assert sut == expected


def test_sort():
    expected = [1, 2, 3]
    sut = Collection([1, 3, 2]).sort()
    assert sut == expected


def test_sort():
    expected = Collection([{'age': 1}, {'age': 2}, {'age': 3}])
    sut = Collection([{'age': 1}, {'age': 3}, {'age': 2}]).sort(lambda x: x['age'])
    assert sut == expected


def test_sort_desc():
    expected = Collection([3, 2, 1])
    sut = Collection([1, 2, 3]).sort_desc()
    assert sut == expected


def test_sort_by():
    expected = Collection([{'age': 1}, {'age': 2}, {'age': 3}])
    sut = Collection([{'age': 1}, {'age': 3}, {'age': 2}]).sort_by('age')
    assert sut == expected


def test_sort_by_desc():
    expected = Collection([{'age': 3}, {'age': 2}, {'age': 1}])
    sut = Collection([{'age': 1}, {'age': 3}, {'age': 2}]).sort_by_desc('age')
    assert sut == expected


def test_splice():
    expected_output = Collection([3, 4])
    expected_collection = Collection([1, 2, 5])
    sut = Collection([1, 2, 3, 4, 5])
    assert sut.splice(2, 2) == expected_output
    assert sut == expected_collection


def test_splice_replace():
    expected_output = Collection([3, 4])
    expected_collection = Collection([1, 2, 0, 0, 5])
    sut = Collection([1, 2, 3, 4, 5])
    assert sut.splice(2, 2, 0) == expected_output
    assert sut == expected_collection


def test_split():
    expected = Collection([[1, 2], [3, 4], [5]])
    sut = Collection([1, 2, 3, 4, 5]).split(3)
    assert sut == expected


def test_take():
    expected = Collection([1, 2])
    sut = Collection([1, 2, 3]).take(2)
    assert sut == expected


def test_take_negative():
    expected = Collection([2, 3])
    sut = Collection([1, 2, 3]).take(-2)
    assert sut == expected


def test_take_while():
    expected = Collection([1, 2])
    sut = Collection([1, 2, 3]).take_until(lambda x: x > 2)
    assert sut == expected


def test_take_until_func():
    expected = Collection([1, 2])
    sut = Collection([1, 2, 3]).take_until(lambda x: x > 2)
    assert sut == expected


def test_take_until_value():
    expected = Collection([1, 2])
    sut = Collection([1, 2, 3]).take_until(3)
    assert sut == expected


def test_take_while():
    expected = Collection([1, 2])
    sut = Collection([1, 2, 3]).take_while(lambda x: x < 3)
    assert sut == expected


def test_tap():
    expected = Collection([1, 2, 3])

    def assert_value(value):
        assert value == expected

    sut = Collection([1, 2, 3]).tap(assert_value)
    assert sut == expected


def test_times():
    expected = Collection([3, 6, 9])
    sut = Collection.times(3, lambda x: x * 3)
    assert sut == expected


def test_transform():
    expected = Collection([3, 6, 9])
    sut = Collection([1, 2, 3]).transform(lambda x: x * 3)
    assert sut == expected


def test_unique():
    expected = Collection([1, 2, 3])
    sut = Collection([1, 1, 1, 2, 2, 3]).unique()
    assert sut == expected

