from collection import Collection


def test_smoke():
    assert Collection([]).items == []


def test_all():
    expected = [1, 2, 3]
    collection = Collection([1, 2, 3])
    print(collection.all() == expected)


def test_avg():
    expected = 3
    assert Collection([1, 5]).avg() == expected


def test_chunk():
    expected = [[1, 2], [3, 4]]
    assert Collection([1, 2, 3, 4]).chunk(2) == expected
