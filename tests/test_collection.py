from context import Collection


class DummyClass:
    def __init__(self, arg):
        self.arg = arg


class TestCollection:
    def test_smoke(self):
        assert Collection([]).items == []

    def test_all(self):
        expected = Collection([1, 2, 3])
        collection = Collection([1, 2, 3])
        print(collection.all() == expected)

    def test_avg(self):
        expected = 3
        assert Collection([1, 5]).avg() == expected

    def test_chunk(self):
        expected = Collection([[1, 2], [3, 4]])
        assert Collection([1, 2, 3, 4]).chunk(2) == expected

    def test_intersect(self):
        expected = Collection([1, 2])
        assert Collection([1, 2, 3, 4]).intersect([1, 2]) == expected

    def test_is_empty(self):
        assert Collection([]).is_empty()

    def test_is_not_empty(self):
        assert Collection([1]).is_not_empty()

    def test_key_by(self):
        expected = Collection([{'a': ['a', 'b']}, {'a': ['a', 'c']}])
        sut = Collection([['a', 'b'], ['a', 'c']]).key_by('a')
        assert sut == expected

    def test_last_none(self):
        assert Collection([]).last() == None

    def test_last_no_arguments(self):
        expected = 1
        assert Collection([3, 2, 1]).last() == expected

    def test_last_function(self):
        expected = 1
        assert Collection([3, 2, 1]).last(lambda x: x > 0) == expected

    def test_map(self):
        expected = Collection([3, 6, 9])
        assert Collection([1, 2, 3]).map(lambda x: x * 3) == expected

    def test_map_into(self):
        expected = DummyClass(1)
        assert type(Collection(1).map_into(DummyClass)[0]) == type(expected)

    def test_map_spread(self):
        expected = Collection([1, 5])
        sut = Collection([0, 1, 2, 3]).chunk(2).map_spread(lambda x, y: x + y)
        assert sut == expected

    def test_max_value(self):
        expected = 3
        sut = Collection([1, 2, 3]).max()
        assert sut == expected

    def test_max_key(self):
        expected = 3
        sut = Collection([{'a': 1}, {'a': 3}]).max(field='a')
        assert sut == expected

    def test_merge(self):
        expected = Collection([1, 2, 3, 4])
        sut = Collection([1, 2]).merge(Collection([3, 4]))
        assert expected == sut

    def test_nth(self):
        expected = Collection(['a', 'c'])
        sut = Collection(['a', 'b', 'c']).nth(2)
        assert sut == expected

    def test_nth_offset(self):
        expected = Collection(['b', 'd'])
        sut = Collection(['a', 'b', 'c', 'd']).nth(2, offset=1)
        assert sut == expected

    def test_pad(self):
        expected = Collection([1, 2, 3, 0])
        sut = Collection([1, 2, 3]).pad(4)
        assert sut == expected

    def test_pad_left_pad_char(self):
        expected = Collection(['x', 1, 2, 3])
        sut = Collection([1, 2, 3]).pad(4, left=True, pad_char='x')
        assert sut == expected

    def test_partition(self):
        expected_odd = Collection([1, 3, 5])
        expected_even = Collection([2, 4, 6])
        actual_even, actual_odd = Collection(
            [1, 2, 3, 4, 5, 6]).partition(lambda x: x % 2 == 0)
        assert expected_even == actual_even
        assert expected_odd == actual_odd

    def test_pop(self):
        expected_collection = Collection([1, 2])
        expected_last_item = 3
        sut = Collection([1, 2, 3])
        last_item = sut.pop()
        assert sut == expected_collection
        assert last_item == expected_last_item

    def test_prepend(self):
        expected = Collection([0, 1, 2])
        sut = Collection([1, 2]).prepend(0)
        assert sut == expected

    def test_append(self):
        expected = Collection([1, 2, 3])
        sut = Collection([1, 2]).push(3)
        assert sut == expected

    def test_random(self):
        expected_results = [1, 2]
        sut = Collection([1, 2]).random(1)
        assert sut in expected_results

    def test_random_multiple(self):
        expected_results = [1, 2, 3]
        sut = Collection([1, 2, 3]).random(2)
        assert sut[0] in expected_results
        assert sut[1] in expected_results

    def test_reject(self):
        expected = Collection([1, 2, 3])
        sut = Collection([1, 2, 3, 4, 5, 6]).reject(lambda x: x > 3)
        assert sut == expected

    def test_reverse(self):
        expected = Collection([3, 2, 1])
        sut = Collection([1, 2, 3]).reverse()
        assert sut == expected

    def test_search(self):
        expected = 1
        sut = Collection([1, 2, 3]).search(2)
        assert sut == expected

    def test_shift(self):
        expected = Collection([2, 3])
        sut = Collection([1, 2, 3])
        assert sut.shift() == expected
        assert sut == expected

    def test_shuffle(self):
        expected_result = Collection([1, 2])
        other_expected_result = Collection([2, 1])
        sut = Collection([1, 2]).shuffle()
        assert sut == expected_result or sut == other_expected_result

    def test_skip_until(self):
        expected = Collection([3, 1])
        sut = Collection([2, 1, 1, 1, 2, 3, 1]).skip_until(lambda x: x > 2)
        assert sut == expected

    def test_skip_while(self):
        expected = Collection([3, 5, 1])
        sut = Collection([2, 1, 1, 1, 2, 3, 3, 5, 1]
                         ).skip_while(lambda x: x > 2)
        assert sut == expected

    def test_slice(self):
        expected = Collection([2, 3])
        sut = Collection([1, 2, 3, 4]).slice(1, 2)
        assert sut == expected

    def test_sort(self):
        expected = [1, 2, 3]
        sut = Collection([1, 3, 2]).sort()
        assert sut == expected

    def test_sort(self):
        expected = Collection([{'age': 1}, {'age': 2}, {'age': 3}])
        sut = Collection([{'age': 1}, {'age': 3}, {'age': 2}]
                         ).sort(lambda x: x['age'])
        assert sut == expected

    def test_sort_desc(self):
        expected = Collection([3, 2, 1])
        sut = Collection([1, 2, 3]).sort_desc()
        assert sut == expected

    def test_sort_by(self):
        expected = Collection([{'age': 1}, {'age': 2}, {'age': 3}])
        sut = Collection([{'age': 1}, {'age': 3}, {'age': 2}]).sort_by('age')
        assert sut == expected

    def test_sort_by_desc(self):
        expected = Collection([{'age': 3}, {'age': 2}, {'age': 1}])
        sut = Collection([{'age': 1}, {'age': 3}, {'age': 2}]
                         ).sort_by_desc('age')
        assert sut == expected

    def test_splice(self):
        expected_output = Collection([3, 4])
        expected_collection = Collection([1, 2, 5])
        sut = Collection([1, 2, 3, 4, 5])
        assert sut.splice(2, 2) == expected_output
        assert sut == expected_collection

    def test_splice_replace(self):
        expected_output = Collection([3, 4])
        expected_collection = Collection([1, 2, 0, 0, 5])
        sut = Collection([1, 2, 3, 4, 5])
        assert sut.splice(2, 2, 0) == expected_output
        assert sut == expected_collection

    def test_split(self):
        expected = Collection([[1, 2], [3, 4], [5]])
        sut = Collection([1, 2, 3, 4, 5]).split(3)
        assert sut == expected

    def test_take(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2, 3]).take(2)
        assert sut == expected

    def test_take_negative(self):
        expected = Collection([2, 3])
        sut = Collection([1, 2, 3]).take(-2)
        assert sut == expected

    def test_take_until(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2, 3]).take_until(lambda x: x > 2)
        assert sut == expected

    def test_take_until_func(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2, 3]).take_until(lambda x: x > 2)
        assert sut == expected

    def test_take_until_value(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2, 3]).take_until(3)
        assert sut == expected

    def test_take_while(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2, 3]).take_while(lambda x: x < 3)
        assert sut == expected

    def test_tap(self):
        expected = Collection([1, 2, 3])

        def assert_value(value):
            assert value == expected

        sut = Collection([1, 2, 3]).tap(assert_value)
        assert sut == expected

    def test_times(self):
        expected = Collection([3, 6, 9])
        sut = Collection.times(3, lambda x: x * 3)
        assert sut == expected

    def test_transform(self):
        expected = Collection([3, 6, 9])
        sut = Collection([1, 2, 3]).transform(lambda x: x * 3)
        assert sut == expected

    def test_unique(self):
        expected = Collection([1, 2, 3])
        sut = Collection([1, 1, 1, 2, 2, 3]).unique()
        assert sut == expected

    def test_unless_false(self):
        expected = Collection([1, 2, 3])
        sut = Collection([1, 2]).unless(False, lambda x: x.push(3))
        assert sut == expected

    def test_unless_true(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2]).unless(True, lambda x: x.push(3))
        assert sut == expected

    def test_unwrap_collection(self):
        expected = 1
        sut = Collection.unwrap(Collection(1))
        assert sut == expected

    def test_unwrap_value(self):
        expected = 1
        sut = Collection.unwrap(1)
        assert sut == expected

    def test_when_true(self):
        expected = Collection([1, 2, 3])
        sut = Collection([1, 2]).when(True, lambda x: x.push(3))
        assert sut == expected

    def test_when_false(self):
        expected = Collection([1, 2])
        sut = Collection([1, 2]).when(False, lambda x: x.push(3))
        assert sut == expected

    def test_when_empty(self):
        expected = Collection([1])
        sut = Collection([]).when_empty(lambda x: x.push(1))
        assert sut == expected

    def test_when_not_empty(self):
        expected = Collection([1, 1])
        sut = Collection([1]).when_not_empty(lambda x: x.push(1))
        assert sut == expected

    def test_where(self):
        expected = Collection([{'apple': 0}])
        sut = Collection([{'apple': 1}, {'apple': 0}]).where('apple', 0)
        assert sut == expected

    def test_where_between(self):
        expected = Collection([{'apple': 2}, {'apple': 3}])
        sut = Collection([
            {'apple': 1},
            {'apple': 2},
            {'apple': 3},
            {'apple': 4}
        ]).where_between('apple', [2, 3])
        assert sut == expected

    def test_where_in(self):
        expected = Collection([{'apple': 2}, {'apple': 3}])
        sut = Collection([
            {'apple': 1},
            {'apple': 2},
            {'apple': 3},
            {'apple': 4}
        ]).where_in('apple', [2, 3])
        assert sut == expected

    def test_where_instance_of(self):
        expected = Collection([DummyClass(1)])
        sut = Collection([DummyClass(1), Collection([1, 2, 3])]
                         ).where_instance_of(DummyClass)
        assert len(sut) == len(expected)
        assert isinstance(sut[0], DummyClass)

    def test_where_not_between(self):
        expected = Collection([{'apple': 1}, {'apple': 4}])
        sut = Collection([
            {'apple': 1},
            {'apple': 2},
            {'apple': 3},
            {'apple': 4}
        ]).where_not_between('apple', [2, 3])
        assert sut == expected

    def test_where_not_in(self):
        expected = Collection([{'apple': 2}, {'apple': 3}])
        sut = Collection([
            {'apple': 1},
            {'apple': 2},
            {'apple': 3},
            {'apple': 4}
        ]).where_not_in('apple', [1, 4])
        assert sut == expected

    def test_where_not_null(self):
        expected = Collection([1, 2, 3])
        sut = Collection([None, 1, 2, 3]).where_not_null()
        assert sut == expected

    def test_where_null(self):
        expected = Collection([None])
        sut = Collection([None, 1, 2, 3]).where_null()
        assert sut == expected

    def test_wrap(self):
        expected = Collection([1])
        sut = Collection.wrap(1)
        assert sut == expected

    def test_zip(self):
        expected = Collection([(1, 2), (3, 4)])
        sut = Collection([1, 3]).zip([2, 4])
        assert sut == expected

    def test_to_json(self):
        expected = '[1, 2, 3]'
        sut = Collection([1, 2, 3]).to_json()
        assert sut == expected

    def test_smoke(self):
        expected = Collection({'a': 1, 'b': 2})
        sut = Collection({'a': 1, 'b': 2})
        assert sut == expected

    def test_diff_assoc(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1}).diff_assoc({'b': 2})
        assert sut == expected

    def test_diff_keys(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1}).diff_keys({'b': 1})
        assert sut == expected

    def test_except_for(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1, 'b': 2}).except_for(['b'])
        assert sut == expected

    def test_keys(self):
        expected = Collection(['a', 'b'])
        sut = Collection({'a': 1, 'b': 2}).keys()
        assert sut == expected

    def test_map_dict(self):
        expected = Collection({'a': 3})
        sut = Collection({'a': 1}).map(lambda x, y: (x, y * 3))
        assert sut == expected

    def test_filter_dict(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1, 'b': 2}).filter(lambda x, y: y < 2)
        assert sut == expected

    def test_flip(self):
        expected = Collection({1: 'a'})
        sut = Collection({'a': 1}).flip()
        assert sut == expected

    def test_forget(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1, 'b': 2}).forget('b')
        assert sut == expected

    def test_get(self):
        expected = 2
        sut = Collection({'a': 1, 'b': 2}).get('b')
        assert sut == expected

    def test_has(self):
        expected = True
        sut = Collection({'a': 1}).has('a')
        assert sut == expected

    def test_intersect_by_keys(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1, 'b': 2}).intersect_by_keys({'a': 2, 'c': 3})
        assert sut == expected

    def test_map_to_groups(self):
        expected = Collection({'a': [1, 2], 'b': [3]})
        sut = Collection([{'name': 'a', 'value': 1},
                          {'name': 'a', 'value': 2},
                          {'name': 'b', 'value': 3}]) \
            .map_to_groups(lambda x: {x['name']: x['value']})
        assert sut == expected

    def test_map_with_keys(self):
        expected = Collection({'a': 1, 'b': 2})
        sut = Collection([{'name': 'a', 'value': 1},
                          {'name': 'b', 'value': 2}])\
            .map_with_keys(lambda x: {x['name']: x['value']})
        assert sut == expected

    def test_only(self):
        expected = Collection({'a': 1})
        sut = Collection({'a': 1, 'b': 2}).only(['a'])
        assert sut == expected

    def test_pull(self):
        expected_return = 1
        expected_collection = Collection({'b': 2})
        sut = Collection({'a': 1, 'b': 2})
        value = sut.pull('a')
        assert sut == expected_collection
        assert expected_return == value

    def test_put(self):
        expected = Collection({'a': 1, 'b': 2})
        sut = Collection({'a': 1}).put('b', 2)
        assert sut == expected

    def test_replace(self):
        expected = Collection(['a', 'c'])
        sut = Collection(['a', 'b']).replace({1: 'c'})
        assert sut == expected

    def test_replace_recursive(self):
        expected = Collection(['a', 'c', ['b']])
        sut = Collection(['a', 'd', ['e']])\
            .replace_recursive({1: 'c', 2: {0: 'b'}})
        assert sut == expected

    def test_sort_by_keys(self):
        expected = Collection({'a': 2, 'b': 1})
        sut = Collection({'b': 1, 'a': 2}).sort_by_keys()
        assert sut == expected

    def test_sort_by_keys_desc(self):
        expected = Collection({'b': 1, 'a': 2})
        sut = Collection({'a': 2, 'b': 1}).sort_by_keys_desc()
        assert sut == expected

    def test_values(self):
        expected = Collection([1, 2, 3])
        sut = Collection({'a': 1, 'b': 2, 'c': 3}).values()
        assert sut == expected

    def test_group_by(self):
        expected = Collection({'a': [{'name': 'a', 'age': 10}]})
        sut = Collection([{'name': 'a', 'age': 10}]).group_by('name')
        assert sut == expected

    def test_cross_join(self):
        expected = Collection([[1, 'a'], [1, 'b'], [2, 'a'], [2, 'b']])
        sut = Collection([1, 2]).cross_join(['a', 'b'])
        assert sut == expected

    def test_each_spread(self):
        expected = [3, 7]
        test_list = []
        Collection([[1, 2], [3, 4]]).each_spread(
            lambda x, y: test_list.append(x + y))
        assert test_list == expected

    def test_each_spread_break(self):
        expected = [3]
        test_list = []

        def sometimes_return_false(x, y):
            if x == 3:
                return False
            else:
                test_list.append(x + y)

        Collection([[1, 2], [3, 4]]).each_spread(sometimes_return_false)
        assert test_list == expected
