from __future__ import annotations
from functools import reduce, wraps
from itertools import chain
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
                         ).filter(lambda x: x[1] > 1)\
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

    @_collect
    def map(self, function: Callable) -> Collection:
        return list(map(function, self.items))

    @_collect
    def reduce(self, function: Callable, accumulator: Any) -> Collection:
        return list(reduce(function, self.items, accumulator))

    @_collect
    def pluck(self, attr: str) -> Collection:
        return list(map(lambda x: x[attr], self.items))

    def sum(self, field: str = None) -> Collection:
        if field:
            return sum(list(map(lambda x: x[field], self.items)))
        else:
            return sum(self.items)

    def to_list(self) -> List:
        return self.items

    @ classmethod
    def make(cls, items) -> Collection:
        return cls(items)

    def __eq__(self, other):
        print(self.items, other)
        return self.items == other

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
