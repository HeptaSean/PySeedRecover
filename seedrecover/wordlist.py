"""Wordlist for BIP-39.

Either the builtin English wordlist (that nearly everybody uses) can be
loaded or a wordlist file can be given to the constructor.
>>> wordlist = Wordlist()

With iterate_all, all words in the word list can be iterated over:
>>> list(wordlist)  # doctest: +ELLIPSIS
['abandon', 'ability', 'able', ..., 'zero', 'zone', 'zoo']
>>> list(wordlist)  # doctest: +ELLIPSIS
['abandon', 'ability', 'able', ..., 'zero', 'zone', 'zoo']

With get_number, the number for a word in the wordlist can be retrieved:
>>> wordlist.get_number("food")
726
>>> wordlist.get_number("foot")
727

If the word is not in the wordlist, a ValueError is raised:
>>> wordlist.get_number("fool")
Traceback (most recent call last):
    ...
ValueError: 'fool' is not in list

With get_word, the word for a number in the range of the wordlist can be
retrieved:
>>> wordlist.get_word(726)
'food'
>>> wordlist.get_word(727)
'foot'

If the number is out of range, an IndexError is raised:
>>> wordlist.get_word(2048)
Traceback (most recent call last):
    ...
IndexError: list index out of range

With contains, a word can be checked if it is in the list:
>>> wordlist.contains("food")
True
>>> wordlist.contains("foot")
True
>>> wordlist.contains("fool")
False

With get_words, the closest words in the list can be retrieved:
>>> wordlist.get_words("food")
['food']
>>> wordlist.get_words("foot")
['foot']
>>> wordlist.get_words("fool")
['cool', 'foil', 'food', 'foot', 'pool', 'tool', 'wool']

If an edit distance is given, all words up to that edit distance are
returned:
>>> wordlist.get_words("food", 1)
['fold', 'food', 'foot', 'good', 'hood', 'wood']
>>> wordlist.get_words("foot", 1)
['food', 'foot']
>>> wordlist.get_words("fool", 1)  # doctest: +NORMALIZE_WHITESPACE
['boil', 'coil', 'cook', 'cool', 'foil', 'fold', 'food', 'foot', 'good',
 'hood', 'oil', 'pool', 'stool', 'tool', 'wood', 'wool']
"""
import pathlib

from typing import Iterator, List, Optional


def edit_distance(a: str, b: str) -> int:
    """Compute the edit distance between strings a and b.

    Uses the optimal string alignment algorithm according to:
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

    >>> edit_distance("abcd", "abcd")
    0
    >>> edit_distance("abcd", "bcd")
    1
    >>> edit_distance("abcd", "abc")
    1
    >>> edit_distance("abcd", "zabcd")
    1
    >>> edit_distance("abcd", "abcdz")
    1
    >>> edit_distance("abcd", "zbcd")
    1
    >>> edit_distance("abcd", "abcz")
    1
    >>> edit_distance("abcd", "bacd")
    1
    >>> edit_distance("abcd", "abdc")
    1
    >>> edit_distance("abcd", "ybcz")
    2
    >>> edit_distance("abcd", "ayzd")
    2
    >>> edit_distance("abc", "ca")
    3
    """
    d = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    for i in range(len(a)+1):
        d[i][0] = i
    for j in range(len(b)+1):
        d[0][j] = j
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            cost = 1
            if a[i-1] == b[j-1]:
                cost = 0
            delete = d[i-1][j] + 1
            insert = d[i][j-1] + 1
            substitute = d[i-1][j-1] + cost
            d[i][j] = min(delete, insert, substitute)
            if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                transpose = d[i-2][j-2] + 1
                d[i][j] = min(d[i][j], transpose)
    return d[len(a)][len(b)]


class Wordlist:
    """Wordlist with similarity functionality."""

    def __init__(self, filename: Optional[str] = None) -> None:
        """Load wordlist from given file (or English if none given)."""
        if not filename:
            filename = str(pathlib.Path(__file__).parent/'english.txt')
        self._words: List[str] = []
        with open(filename) as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                self._words.append(word)

    def __iter__(self) -> Iterator[str]:
        """Return iterator for words in list."""
        return self._words.__iter__()

    def get_number(self, word: str) -> int:
        """Get the number for a given word."""
        return self._words.index(word)

    def get_word(self, number: int) -> str:
        """Get the word for a given number."""
        return self._words[number]

    def contains(self, word: str) -> bool:
        """Check if word is in list."""
        return word in self._words

    def get_words(self, word: str, distance: int = 0) -> List[str]:
        """Get words in list up to edit distance."""
        initial_words = []
        if word in self._words:
            initial_words = [word]
        else:
            closest = None
            for other_word in self._words:
                other_distance = edit_distance(other_word, word)
                if not closest or other_distance < closest:
                    closest = other_distance
                    initial_words = [other_word]
                elif other_distance == closest:
                    initial_words.append(other_word)
        if distance == 0:
            return initial_words
        words = []
        for other_word in self._words:
            for initial_word in initial_words:
                if edit_distance(other_word, initial_word) <= distance:
                    words.append(other_word)
                    break
        return words
