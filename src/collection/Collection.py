from __future__ import annotations
from functools import reduce, wraps
from statistics import median, mode
from collections import Counter
from typing import List, Any, Iterable, Callable, Union


def _collect(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        method_output = method(self, *method_args, **method_kwargs)
        return self.make(method_output)

    return _impl


class Collection:
    def __init__(self, items) -> None:
        self.items = [items] if type(items) != list else items

    @_collect
    def all(self):
        return self.items

    def avg(self, key=None):
        if key:
            return self.make(self.items).pluck(key).sum() / len(self.items)
        return self.make(self.items).sum() / len(self.items)

    @_collect
    def chunk(self, n):
        new_array = []
        for i in range(0, len(self.items), n):
            new_array.append(self.items[i:i + n])
        return new_array

    @_collect
    def combine(self, other):
        return self.make(self.items) + self.make(other)

    def contains(self, item):
        if callable(item):
            return self.make(self.items).first(item) in self.items
        return item in self.items

    def count(self) -> Collection:
        return len(self.items)

    def count_by(self, *func):
        if func:
            items = self.make(self.items).map(func[0])
        else:
            items = self.items
        return Counter(items)

    def dd(self):
        exit(self.make(self.items))

    def diff(self, lst):
        return self.make(self.items).filter(lambda x: x not in lst)

    @_collect
    def duplicates(self):
        return self.make(list(Counter(self.items).items())
                         ).filter(lambda x: x[1] > 1) \
            .map(lambda x: x[0])

    @_collect
    def each(self, function: Callable) -> Collection:
        for item in self.items:
            function(item)
        return self.items

    def every(self, func):
        if not self.items:
            return True
        return self.make(self.items).map(func).contains(False) == False

    @_collect
    def filter(self, function: Callable) -> Collection:
        return list(filter(function, self.items))

    def first(self, *func):
        if not self.items:
            return None
        elif not func:
            return self.items[0]

        for item in self.items:
            if func[0](item):
                return item
        return False

    def firstWhere(self, key, value):
        return self.make(self.items).first(lambda x: x[key] == value)

    @_collect
    def flatten(self, depth=None) -> Collection:
        new_items = []

        def append_item(item, depth):
            new_item = self.make(item) if type(item) != Collection else item
            for i in new_item:
                if type(i) != Collection and type(i) != list:
                    new_items.append(i)
                else:
                    depth = depth - 1 if depth is not None else depth
                    if depth is None or depth != 0:
                        append_item(i, depth)
                    else:
                        new_items.append(i)

        self.make(self.items).each(lambda x: append_item(x, depth))
        return new_items

    def flat_map(self, func):
        return self.flatten().map(func)

    def for_page(self, page, size):
        return self.make(self.items).chunk(size)[page - 1]

    def implode(self, glue):
        return glue.join(self.items)

    def intersect(self, other):
        return self.make(self.items).filter(lambda x: x in other)

    def is_empty(self):
        return len(self.items) == 0

    def is_not_empty(self):
        return len(self.items) > 0

    def key_by(self, key):
        return self.make(self.items).map(lambda x: {key: x})

    @_collect
    def keys(self):
        return list(self.items[0].keys())

    def last(self, *func):
        if not self.items:
            return None
        elif not func:
            return self.items[-1]

        for item in reversed(self.items):
            if func[0](item):
                return item
        return False

    @_collect
    def map(self, function: Callable) -> Collection:
        return list(map(function, self.items))

    @_collect
    def map_into(self, cls):
        return self.make(self.items).map(lambda x: cls(x))

    def map_spread(self, func):
        return self.make(self.items).map(lambda args: func(*args)).flatten()

    def max(self, field=None):
        return self.pluck_and_func(max, field)

    def median(self, field=None):
        return self.pluck_and_func(median, field)

    def mode(self, field=None):
        return self.pluck_and_func(mode, field)

    @_collect
    def merge(self, other):
        try:
            return self + other
        except AttributeError:
            return self.items + other

    def min(self, field=None):
        return self.pluck_and_func(min, field)

    def nth(self, place, offset=0):
        return self.make(self.items) \
            .skip(offset)\
            .pipe(lambda x: list(enumerate(x)))\
            .filter(lambda x: x[0] % place == 0) \
            .map(lambda x: x[1])

    def pad(self, size, left=False, pad_char=0):
        padded = []
        for char in range(size - self.make(self.items).count()):
            if left:
                padded.append(pad_char)
            else:
                self.items.append(pad_char)
        if left:
            padded.append(self.items)
            return self.make(padded).flatten()
        else:
            return self.make(self.items)

    @_collect
    def reduce(self, function: Callable, accumulator: Any) -> Collection:
        return list(reduce(function, self.items, accumulator))

    @_collect
    def pipe(self, func):
        return func(self.items)

    @_collect
    def pluck(self, attr: str) -> Collection:
        return list(map(lambda x: x[attr], self.items))

    @_collect
    def skip(self, offset):
        return self.items[offset:]

    def sum(self, field: str = None) -> Collection:
        return self.pluck_and_func(sum, field)

    def pluck_and_func(self, func, field=None):
        if field:
            return func(self.make(self.items).pluck(field).to_list())
        else:
            return func(self.items)

    def to_list(self) -> List:
        return self.items

    @classmethod
    def make(cls, items) -> Collection:
        return cls(items)

    def __eq__(self, other):
        return self.items == other.items

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.to_list()})'

    def __repr__(self):
        return self.__str__()

    def __len__(self) -> int:
        return self.count()

    def __getitem__(self, key) -> Any:
        return self.items[key]

    def __setitem__(self, key, value) -> None:
        self.items[key] = value

    def __iter__(self) -> Iterable:
        return self.items.__iter__()

    def __add__(self, other):
        return self.items + other.items
