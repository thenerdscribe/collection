from __future__ import annotations

import json
import random
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
        self.og_item = items
        self.items = [items] if type(items) != list else items

    @_collect
    def all(self):
        return self.items

    def append(self, item):
        return self.push(item)

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

    def first_where(self, key, value):
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
            .skip(offset) \
            .enumerate() \
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

    def partition(self, func):
        collection = self.make(self.items)
        true_condition = collection.filter(func)
        false_condition = collection.reject(func)
        return true_condition, false_condition

    def pop(self):
        last_item = self.items.pop()
        return last_item

    def prepend(self, item):
        self.items.insert(0, item)
        return self

    def push(self, item):
        self.items.append(item)
        return self

    @_collect
    def pipe(self, func):
        return func(self.items)

    @_collect
    def pluck(self, attr: str) -> List:
        return list(map(lambda x: x[attr], self.items))

    def random(self, retrieve=1):
        return random.choices(self.items, k=retrieve) if retrieve != 1 else random.choice(self.items)

    @_collect
    def reduce(self, function: Callable, accumulator: Any) -> List:
        return list(reduce(function, self.items, accumulator))

    def reject(self, func):
        return self.make(self.items).filter(lambda x: not func(x))

    @_collect
    def reverse(self):
        return list(reversed(self.items))

    @_collect
    def enumerate(self):
        return list(enumerate(self.items))

    def search(self, search):
        return self.make(self.items) \
            .enumerate() \
            .first(lambda x: search == x[1])[0]

    def shift(self):
        self.items = self.items[1:]
        return self

    @_collect
    def shuffle(self):
        return random.sample(self.items, k=len(self.items))

    @_collect
    def skip(self, offset):
        return self.items[offset:]

    def skip_until(self, func):
        return self.__skip_base(func, 0)

    def skip_while(self, func):
        return self.__skip_base(func, 1)

    def __skip_base(self, func, places):
        collection = self.make(self.items)
        if callable(func):
            place = collection.enumerate().first(lambda x: func(x[1]))[0]
        else:
            place = collection.enumerate().first(lambda x: x[1] == func)[0]
        return collection.skip(place + places)

    def slice(self, position, size=None):
        if not size:
            return self.skip(position)
        else:
            return self.make(self.items[position:position + size])

    def sum(self, field: str = None) -> Collection:
        return self.pluck_and_func(sum, field)

    @_collect
    def sort(self, func=None):
        return sorted(self.items, key=func)

    @_collect
    def sort_desc(self, func=None):
        return sorted(self.items, key=func, reverse=True)

    @_collect
    def sort_by(self, key):
        return sorted(self.items, key=lambda x: x[key])

    @_collect
    def sort_by_desc(self, key):
        return sorted(self.items, key=lambda x: x[key], reverse=True)

    @_collect
    def splice(self, pos, size=0, *args):
        to_return = self.items[pos:pos + size]
        temp_list = []
        for key, item in enumerate(self.items):
            if args and pos <= key < (pos + size):
                self.items[key] = args[0]
            if not pos <= key < (pos + size):
                temp_list.append(item)
        if not args:
            self.items = temp_list
        return to_return

    @_collect
    def split(self, size):
        lists = []
        d, r = divmod(len(self.items), size)
        for i in range(size):
            si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
            lists.append(self.items[si:si + (d + 1 if i < r else d)])
        return lists

    @_collect
    def take(self, count):
        if count > 0:
            return self.items[:count]
        else:
            return self.items[count:]

    @_collect
    def take_while(self, func):
        first = self.make(self.items).first(func)
        return self.items[:first - 1]

    @_collect
    def take_until(self, func):
        collection = self.make(self.items)
        if callable(func):
            place = collection.enumerate().first(lambda x: func(x[1]))[0]
        else:
            place = collection.enumerate().first(lambda x: x[1] == func)[0]
        return self.items[:place]

    @_collect
    def take_while(self, func):
        first = self.make(self.items).first(lambda x: not func(x))
        return self.items[:first - 1]

    def tap(self, func):
        func(self.make(self.items))
        return self

    def pluck_and_func(self, func, field=None):
        if field:
            return func(self.make(self.items).pluck(field).to_list())
        else:
            return func(self.items)

    @classmethod
    def times(cls, times, func):
        new_list = []
        for number in range(1, times + 1):
            new_list.append(func(number))
        return cls(new_list)

    def to_json(self):
        return json.dumps(self.items)

    def transform(self, func):
        self.items = list(map(func, self.items))
        return self

    @_collect
    def unique(self):
        return list(set(self.items))

    def unless(self, condition, func):
        if not condition:
            return func(self.make(self.items))
        else:
            return self

    def unless_empty(self, func):
        return self.when_not_empty(func)

    def unless_not_empty(self, func):
        return self.when_empty(func)

    @staticmethod
    def unwrap(item):
        try:
            return item.og_item
        except AttributeError:
            return item

    def when(self, condition, func):
        if condition:
            return func(self.make(self.items))
        else:
            return self

    def when_not_empty(self, func):
        if len(self.items) != 0:
            return func(self.make(self.items))
        else:
            return self

    def when_empty(self, func):
        if len(self.items) == 0:
            return func(self.make(self.items))
        else:
            return self

    def where(self, key, value):
        return self.make(self.items).filter(lambda x: x[key] == value)

    def where_between(self, key, range_list):
        return self.make(self.items).filter(lambda x: range_list[0] <= x[key] <= range_list[1])

    def where_in(self, key, options):
        return self.make(self.items).filter(lambda x: x[key] in options)

    def where_instance_of(self, cls):
        return self.make(self.items).filter(lambda x: isinstance(x, cls))

    def where_not_between(self, key, range_list):
        return self.make(self.items).filter(lambda x: not range_list[0] <= x[key] <= range_list[1])

    def where_not_in(self, key, options):
        return self.make(self.items).filter(lambda x: x[key] not in options)

    def where_not_null(self):
        return self.make(self.items).filter(lambda x: x is not None)

    def where_null(self):
        return self.make(self.items).filter(lambda x: x is None)

    @classmethod
    def wrap(cls, item):
        if isinstance(item, cls):
            return item
        else:
            return cls(item)

    @_collect
    def zip(self, other):
        return list(zip(self.items, other))

    def to_list(self) -> List:
        return self.items

    @classmethod
    def make(cls, items) -> Collection:
        if isinstance(items, cls):
            return items
        else:
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
