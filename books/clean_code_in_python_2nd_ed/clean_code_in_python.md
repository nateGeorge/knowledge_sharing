Nathan George | Tink AB | July 24, 2022

# Summary of "Clean Code in Python"

[comment]: # (!!!)

<img src="media/clean_code_cover.png" alt="book cover" width="500"/>


[comment]: # (!!!)

Code is generally written to communicate with machines, but we also largely use it to communicate with other developers. Hence why clean and standardized code is important.

[comment]: # (!!!)

Consistent code formatting makes searching for things easier. PEP8 is the standard in Python. Example:
searching for an argument named location: `grep -nr "location="`
searching for a variable called "location" being set: `grep -nr "location = "`

[comment]: # (!!!)

"code comments are evil"

Aim to have as few code comments as possible.

"comments in code are a symptom of our
inability to express our code correctly"

Code should be self-documenting:
- variable names describe what they are
- function names describe what they do

Try to rewrite comments with code (e.g. changing variable name, adding a function)

"Mercilessly" delete commented-out code. It can be saved in a Git history instead.

[comment]: # (!!!)

Annotations can be used to have built-in docs in code.

Consider these two:

```python
def launch_task(delay_in_seconds):
...
```

```python
Seconds = float
def launch_task(delay: Seconds):
...
```

In the second, we see that the delay is in seconds, and can be fractional.

We can also use these annotations for automated checks (generate docs, run validations, enforcec checks). E.g. `locate.__annotations__` gives a dict with inputs/outputs of a function and their types.

[comment]: # (!!!)

# Automated checks

Add to build (CI)
- type consistency (mypy, pytype)
    - mypy checks defs against args
    - pytype checks if types at runtime will be correct
- linting
    - pycodestyle, flake8, pylint, Coala
    - pylint maybe best for Python, Coala for multiple languages
- autoformatting
    - black (more restrictive, subset of PEP8), autopep8, yapf (highly customizable, partial formatting of files)
    - can use "milestone" commit to apply black to everything, or apply black to each commit and rewrite history
    - yapf can be used to only format new additions to code
- use a makefile for easy-to-use CI steps that can be reused and modified

[comment]: # (!!!)

Idioms: a way to write code for a particular task
Design patterns: high-level ideas for implementing something, independent from the language

Pythonic idioms:
- better performance
- more compact
- easier to understand

[comment]: # (!!!)

# Context managers (Python idiom)
- `contextlib` module, `contextmanager` decorator, `contextlib.ContextDecorator` for inheritance
- e.g. `with` - these have `__enter__` and `__exit__` methods
    - `__exit__` always called at the end or if there is an exception
- used for opening files, connections, managing resources
- e.g. backup database
- `__exit__` takes values from exception, if no exception, they are `None`

```python
class DBHandler:
    def __enter__(self):
        stop_database()
        return self
    
    def __exit__(self, exc_type, ex_value, ex_traceback):
        start_database()

with DBHandler():
    db_backup()
```

[comment]: # (!!!)

# List comprehensions

Use instead of loops when it increases readability and reliability (also slightly faster but not noticible). Example:

```python
def collect_account_ids_from_arns(arns: Iterable[str]) -> Set[str]:
    collected_account_ids = set()
    for arn in arns:
    matched = re.match(ARN_REGEX, arn)
    if matched is not None:
    account_id = matched.groupdict()["account_id"]
    collected_account_ids.add(account_id)
    return collected_account_ids
```

```python
def collect_account_ids_from_arns(arns):
    matched_arns = filter(None, (re.match(ARN_REGEX, arn) for arn in arns))
    return {m.groupdict()["account_id"] for m in matched_arns}
```

[comment]: # (!!!)

# PEP572 and assignment expressions
Allows for even more compact list/dict/set comprehensions:

```python
def collect_account_ids_from_arns(arns: Iterable[str]) -> Set[str]:
    return {
    matched.groupdict()["account_id"]
    for arn in arns
    if (matched := re.match(ARN_REGEX, arn)) is not None
    }
```

[comment]: # (!!!)

# Private, public, protected
Other languages have private and protected functions, but everything in Python is public. A convention is to begin a function name with an underscore if intended to be private.

If it's not intended to be used externally, keep it private. This makes refactoring the code easier, since the private methods should only be used within the class and not all over the place in many different ways.

Double underscore doesn't make it private, but is a misconception. Instead, it will get "name mangled" like `"_<class-name>__<attributename>`. Don't use this, and don't use "dunder" methods (2 underscore before/after) for methods. Just use a single underscore and respect the convention that those are private attrs/methods.


[comment]: $ (!!!)

We can set validation for properties like so (e.g. in a class):

```python
@property
    def latitude(self) -> float:
    return self._latitude

@latitude.setter
def latitude(self, lat_value: float) -> None:
    if lat_value not in range(-90, 90 + 1):
        raise ValueError(f"{lat_value} is an invalid value for
            latitude")
    self._latitude = lat_value
```

[comment]: $ (!!!)

# Command and query separation of objects

"The command and query separation principle states that a method of an object should either answer to something or do something, but not both."

"don't do more than one thing in a method"

"If you want to assign something and then check
the value, break that down into two or more statements."

"try to make properties idempotent" - e.g. we can get properties multiple times and not change the state


[comment]: $ (!!!)

# dataclass decorator

Possible to use this to avoid some __init__ boilerplace, although this is a confusing example. Best suited "for data classes would be all those places when we need
to use objects as data containers or wrappers, namely situations on which we used
named tuples or simple namespaces."

```python
from typing import List
from dataclasses import dataclass, field

R = 26

@dataclass
class RTrieNode:
    size = R
    value: int
    next_: List["RTrieNode"] = field(
    default_factory=lambda: [None] * R)
    
    def __post_init__(self):
        if len(self.next_) != self.size:
        raise ValueError(f"Invalid length provided for next list")
```

[comment]: $ (!!!)

# Making your own iterables

Needs:
- `__next__` or `__iter__`
- `__len__` and `__getitem__`

```python
from datetime import timedelta

class DateRangeIterable:
    """An iterable that contains its own iterator object."""
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration()
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today
```

```python
>>> from datetime import date
>>> for day in DateRangeIterable(date(2018, 1, 1), date(2018, 1, 5)):
... print(day)
...
2018-01-01
2018-01-02
2018-01-03
2018-01-04
```

First calls the iter method, which indicates it's iterable by returning itself. Then calls next until it gets a StopIteration exception.

One issue is if the iterable has been used, you can't use it again without recreating it. We can return a new instance of it or a generator to fix this:

```python
def __iter__(self):
    current_day = self.start_date
    while current_day < self.end_date:
        yield current_day
        current_day += timedelta(days=1)
```

Then we can create it multiple times and use it. Called a "container iterable".

```python
>>> r1 = DateRangeContainerIterable(date(2018, 1, 1), date(2018, 1, 5))
>>> ", ".join(map(str, r1))
'2018-01-01, 2018-01-02, 2018-01-03, 2018-01-04'
>>> max(r1)
datetime.date(2018, 1, 4)
```

[comment]: $ (!!!)

# Iterable vs sequence

An iterable, like we saw before, uses less memory but more CPU. To get the nth value, we have to iterate n times. Sequences store it all in memory so use less CPU but more memory. We can define the len and get_item methods, but not the iter method to create a sequence:

```python
class DateRangeSequence:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._range = self._create_range()
    
    def _create_range(self):
        days = []
        current_day = self.start_date
        while current_day < self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days

    def __getitem__(self, day_no):
        return self._range[day_no]

    def __len__(self):
        return len(self._range)
```

Now we can index the item instead of looping through each time to get different elements.

[comment]: $ (!!!)

# Container objects

Like a set, has a `x in y` method from `__contains__`
- Implement the `__contains__` method, which gets called with `in`

[comment]: $ (!!!)

# __getattr__

Used when getting attributes that aren't part of the class.


```python
class DynamicAttributes:
    def __init__(self, attribute):
        self.attribute = attribute

    def __getattr__(self, attr):
        if attr.startswith("fallback_"):
            name = attr.replace("fallback_", "")
            return f"[fallback resolved] {name}"
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute {attr}"
        )
```

"if you're creating a wrapper object on top
of another one by means of composition, and you want to delegate most of the
methods to the wrapped object, instead of copying and defining all of those methods,
you can implement __getattr__ that will internally call the same method on the
wrapped object."

"Use the __getattr__ magic method when you see an opportunity to avoid lots of
duplicated code and boilerplate, but don't abuse this method"

- code compactness vs maintainability

[comment]: $ (!!!)

# Callable objects

"The magic method __call__ will be called when we try to execute our object as if
it were a regular function. Every argument passed to it will be passed along to the
__call__ method."

If we want to save the state between calls. Handy for decorators.

```python
from collections import defaultdict

class CallCount:
    def __init__(self):
        self._counts = defaultdict(int)

    def __call__(self, argument):
        self._counts[argument] += 1
        return self._counts[argument]
```

```python
>>> cc = CallCount()
>>> cc(1)
1
>>> cc(2)
1
>>> cc(1)
```

[comment]: $ (!!!)

<img src="media/magic_methods_cheat_sheet.png" alt="magic methods" width="500"/>

Use these by declaring a class from `collections.abc` with the corresponding type, and provides methods and types for what you want.

[comment]: $ (!!!)

# Caveats, things to avoid

- mutable default args
- use `collections` module to extend built-in types
[comment]: $ (!!!)

# Mutable default args

```python
def wrong_user_display(user_metadata: dict = {"name": "John", "age":
30}):
    name = user_metadata.pop("name")
```

Dict is created once when the file is run. Instead, do this:

```python
def user_display(user_metadata: dict = None):
    user_metadata = user_metadata or {"name": "John", "age": 30}
    name = user_metadata.pop("name")
```


[comment]: $ (!!!)

# use `collections` module to extend built-in types

"in CPython
(a C optimization), the methods of the class don't call each other (as they should),
so if you override one of them, this will not be reflected by the rest"

"you might want to override __getitem__, and
then when you iterate the object with a for loop, you will notice that the logic you
have put on that method is not applied."

"Don't extend directly from dict; use collections.UserDict
instead. For lists, use collections.UserList, and for strings, use
collections.UserString."

```python
from collections import UserList

class GoodList(UserList):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        if index % 2 == 0:
            prefix = "even"
        else:
            prefix = "odd"

        return f"[{prefix}] {value}"
```
[comment]: $ (!!!)

# Asynchronous code

The advantage is to not block I/O operations.

Async modules/libraries:
- asyncio
- trio
- curio

Uses *coroutines*. Like functions, but declared with something like `async def`. When calling another one from inside a coroutine, use `await`. Then the "event loop" continues.

```python

async def mycoro(*args, **kwargs):
    # … logic
    await third_party.coroutine(…)
    # … more of our logic

result = await mycoro(…)
```

Or

```python
import asyncio

asyncio.run(mycoro(…))
```

[comment]: $ (!!!)

# 


[comment]: $ (!!!)
[comment]: $ (!!!)
[comment]: $ (!!!)



[comment]: # (!!!)

Other funny tidbits:
- `slice()` is a function that can be used to index iterables (e.g. `a = list[1, 2, 3]`, `a[slice(None, 2, 2)]` is the same as `a[:2:2]`)

