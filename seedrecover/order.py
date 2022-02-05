"""Permutations, combinations, and extensions of given lists."""
from typing import TypeVar, Iterable, Iterator

X = TypeVar('X')


def permute(lst: list[X]) -> Iterator[list[X]]:
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


def combine(lst: list[list[X]]) -> Iterator[list[X]]:
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


def extend(given: list[X], allx: Iterable[X], length: int,
           positions: list[int]) -> Iterator[list[X]]:
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


def iterate(given: list[list[X]], perm: bool, allx: Iterable[X],
            length: int, positions: list[int]) -> Iterator[list[X]]:
    """Combine, permute, and extend the given data."""
    if perm:
        for permutation in permute(given):
            for combination in combine(permutation):
                for extension in extend(combination, allx, length, positions):
                    yield extension
    else:
        for combination in combine(given):
            for extension in extend(combination, allx, length, positions):
                yield extension