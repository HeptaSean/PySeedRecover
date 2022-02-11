"""Permutations, combinations, and extensions of given lists.

The iterate function can do all of the variations together.
* The first argument is a list of lists of possible values for each position.
* The second argument decides if reorderings of the given values should be
  done.
* The third argument is an iterable of all values to be tried in missing
  positions. The fourth arguments is the total target length and the fifth
  argument is a list of positions (of the final lists) to try as missing
  positions.
>>> list(iterate([["fst1", "fst2"], ["scd1"], ["thd1"]], False,
...              ["all1", "all2"], 4, [0,3]))  # doctest: +NORMALIZE_WHITESPACE
[['all1', 'fst1', 'scd1', 'thd1'], ['all2', 'fst1', 'scd1', 'thd1'],
 ['fst1', 'scd1', 'thd1', 'all1'], ['fst1', 'scd1', 'thd1', 'all2'],
 ['all1', 'fst2', 'scd1', 'thd1'], ['all2', 'fst2', 'scd1', 'thd1'],
 ['fst2', 'scd1', 'thd1', 'all1'], ['fst2', 'scd1', 'thd1', 'all2']]
>>> list(iterate([["fst1", "fst2"], ["scd1"], ["thd1"]], True,
...              ["all1", "all2"], 4, [0,3]))  # doctest: +NORMALIZE_WHITESPACE
[['all1', 'fst1', 'scd1', 'thd1'], ['all2', 'fst1', 'scd1', 'thd1'],
 ['fst1', 'scd1', 'thd1', 'all1'], ['fst1', 'scd1', 'thd1', 'all2'],
 ['all1', 'fst2', 'scd1', 'thd1'], ['all2', 'fst2', 'scd1', 'thd1'],
 ['fst2', 'scd1', 'thd1', 'all1'], ['fst2', 'scd1', 'thd1', 'all2'],
 ['all1', 'fst1', 'thd1', 'scd1'], ['all2', 'fst1', 'thd1', 'scd1'],
 ['fst1', 'thd1', 'scd1', 'all1'], ['fst1', 'thd1', 'scd1', 'all2'],
 ['all1', 'fst2', 'thd1', 'scd1'], ['all2', 'fst2', 'thd1', 'scd1'],
 ['fst2', 'thd1', 'scd1', 'all1'], ['fst2', 'thd1', 'scd1', 'all2']]
"""
from typing import Iterable, Iterator, List, TypeVar

X = TypeVar('X')


def permute(lst: List[X]) -> Iterator[List[X]]:
    """Permute the given list and yield all permutations.

    >>> list(permute([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    if lst == []:
        yield []
    else:
        for i in range(len(lst)):
            for permutation in permute(lst[:i] + lst[i+1:]):
                yield [lst[i]] + permutation


def reorder(lst: List[X]) -> Iterator[List[X]]:
    """Compute plausible reorderings of the given list and yield them.

    We consider a reordering plausible if it always jumps to the n-th
    element of the given list (representing confusion of rows and columns).
    A list of [1, 2, 3, 4, 5, 6, 7] could have been read row-wise from:
    1 2  or  1 2 3  or  1 2 3 4  or  1 2 3 4 5  or  1 2 3 4 5 6
    3 4      4 5 6      5 6 7        6 7            7
    5 6      7
    7

    Reading these arrangements column-wise leads to the following reorderings
    with the original ordering first:
    >>> list(reorder([1, 2, 3, 4, 5, 6, 7]))  # doctest: +NORMALIZE_WHITESPACE
    [[1, 2, 3, 4, 5, 6, 7], [1, 3, 5, 7, 2, 4, 6], [1, 4, 7, 2, 5, 3, 6],
     [1, 5, 2, 6, 3, 7, 4], [1, 6, 2, 7, 3, 4, 5], [1, 7, 2, 3, 4, 5, 6]]
    """
    for jump in range(1, len(lst)):
        reordering = []
        for start in range(jump):
            offset = 0
            while start + offset < len(lst):
                reordering.append(lst[start + offset])
                offset += jump
        yield reordering


def combine(lst: List[List[X]]) -> Iterator[List[X]]:
    """Combine elements from each of the sublists and yield all combinations.

    >>> list(combine([[1, 2, 3], [1], [1, 2]]))
    [[1, 1, 1], [1, 1, 2], [2, 1, 1], [2, 1, 2], [3, 1, 1], [3, 1, 2]]
    """
    if lst == []:
        yield []
    else:
        for first in lst[0]:
            for combination in combine(lst[1:]):
                yield [first] + combination


def extend(given: List[X], allx: Iterable[X], length: int,
           positions: List[int]) -> Iterator[List[X]]:
    """Extend the given list at given positions with all possible elements.

    >>> list(extend([1, 2, 3, 4, 5], [8, 9],
    ...             7, [0, 3, 6]))  # doctest: +NORMALIZE_WHITESPACE
    [[8, 1, 2, 8, 3, 4, 5], [8, 1, 2, 9, 3, 4, 5],
     [8, 1, 2, 3, 4, 5, 8], [8, 1, 2, 3, 4, 5, 9],
     [9, 1, 2, 8, 3, 4, 5], [9, 1, 2, 9, 3, 4, 5],
     [9, 1, 2, 3, 4, 5, 8], [9, 1, 2, 3, 4, 5, 9],
     [1, 2, 3, 8, 4, 5, 8], [1, 2, 3, 8, 4, 5, 9],
     [1, 2, 3, 9, 4, 5, 8], [1, 2, 3, 9, 4, 5, 9]]
    """
    if length == len(given):
        yield given
    else:
        missing = length - len(given)
        last_first_position = len(positions) - missing + 1
        for i in range(last_first_position):
            position = positions[i]
            rest_length = length - position - 1
            rest_positions = [p - position - 1 for p in positions[i+1:]]
            for x in allx:
                for extension in extend(given[position:], allx,
                                        rest_length, rest_positions):
                    yield given[:position] + [x] + extension


def iterate(given: List[List[X]], perm: bool, allx: Iterable[X],
            length: int, positions: List[int]) -> Iterator[List[X]]:
    """Combine, permute, and extend the given data."""
    if perm:
        for reordering in reorder(given):
            for combination in combine(reordering):
                for extension in extend(combination, allx, length, positions):
                    yield extension
    else:
        for combination in combine(given):
            for extension in extend(combination, allx, length, positions):
                yield extension
