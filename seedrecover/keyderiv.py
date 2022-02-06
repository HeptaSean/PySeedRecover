"""Cardano key derivation from seed phrases.

>>> wordlist = Wordlist()
"""
import hashlib

from seedrecover.wordlist import Wordlist

from typing import Iterable


class ChecksumError(Exception):
    """Raised if checksum of seed phrase is not correct."""

    pass


def seed2entropy(seed: Iterable[str], wordlist: Wordlist) -> bytes:
    """Derive entropy from seed phrase.

    Algorithm is described in:
    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

    >>> wordlist = Wordlist()

    If the checksum is wrong, a ChecksumError is raised:
    >>> seed2entropy(["abandon", "abandon", "abandon", "abandon", "abandon",
    ...               "abandon", "abandon", "abandon", "abandon", "abandon",
    ...               "abandon", "abandon"], wordlist).hex()
    Traceback (most recent call last):
        ...
    keyderiv.ChecksumError

    Test vectors linked in the BIP:
    >>> seed2entropy(["abandon", "abandon", "abandon", "abandon", "abandon",
    ...               "abandon", "abandon", "abandon", "abandon", "abandon",
    ...               "abandon", "about"], wordlist).hex()
    '00000000000000000000000000000000'
    >>> seed2entropy(["legal", "winner", "thank", "year", "wave",
    ...               "sausage", "worth", "useful", "legal", "winner",
    ...               "thank", "yellow"], wordlist).hex()
    '7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f'
    >>> seed2entropy(["letter", "advice", "cage", "absurd", "amount",
    ...               "doctor", "acoustic", "avoid", "letter", "advice",
    ...               "cage", "above"], wordlist).hex()
    '80808080808080808080808080808080'
    >>> seed2entropy(["zoo", "zoo", "zoo", "zoo", "zoo",
    ...               "zoo", "zoo", "zoo", "zoo", "zoo",
    ...               "zoo", "wrong"], wordlist).hex()
    'ffffffffffffffffffffffffffffffff'

    Test vector for master key derivation (see entropy2masterkey):
    >>> seed2entropy(["eight", "country", "switch", "draw", "meat",
    ...               "scout", "mystery", "blade", "tip", "drift",
    ...               "useless", "good", "keep", "usage", "title"],
    ...               wordlist).hex()
    '46e62370a138a182a498b8e2885bc032379ddf38'

    Test wallets of PySeedRecover:
    >>> seed2entropy(["ladder", "long", "kangaroo", "inherit", "unknown",
    ...               "prize", "else", "second", "enter", "addict",
    ...               "mystery", "valve", "riot", "attitude", "area",
    ...               "blind", "fabric", "symbol", "skill", "sunset",
    ...               "goose", "shock", "gasp", "grape"],
    ...               wordlist).hex()
    '7c7079e639eedf56920e134b606a49f88ba21d42d0be517b8f29ecc6498c980b'
    >>> seed2entropy(["ladder", "long", "kangaroo", "inherit", "unknown",
    ...               "prize", "else", "second", "enter", "addict",
    ...               "mystery", "valve", "riot", "attitude", "area",
    ...               "blind", "fabric", "symbol", "skill", "sunset",
    ...               "goose", "shock", "gasp", "uphold"],
    ...               wordlist).hex()
    '7c7079e639eedf56920e134b606a49f88ba21d42d0be517b8f29ecc6498c980f'
    """
    entropy = bytearray()
    bits = 0
    rest = 0
    for word in seed:
        number = wordlist.get_number(word)
        byte = rest << 8 - bits | number >> 3 + bits
        entropy.append(byte)
        bits += 3
        rest = number & (1 << bits) - 1
        if bits > 8:
            entropy.append(rest >> bits - 8)
            bits -= 8
            rest = number & (1 << bits) - 1
    sha256 = hashlib.sha256()
    sha256.update(entropy)
    first_byte = sha256.digest()[0]
    bits = len(entropy) // 4
    if first_byte >> 8 - bits != rest:
        raise ChecksumError()
    return entropy


def entropy2masterkey(entropy: bytes) -> bytes:
    """Derive master key from entropy.

    Algorithm is described in:
    https://github.com/cardano-foundation/CIPs/blob/master/CIP-0003/Icarus.md

    Test vector from the CIP:
    >>> e = bytes.fromhex('46e62370a138a182a498b8e2885bc032379ddf38')
    >>> entropy2masterkey(e).hex()  # doctest: +NORMALIZE_WHITESPACE
    'c065afd2832cd8b087c4d9ab7011f481ee1e0721e78ea5dd609f3ab3f156d245d176bd\
8fd4ec60b4731c3918a2a72a0226c0cd119ec35b47e4d55884667f552a23f7fdcd4a10c6cd2\
c7393ac61d877873e248f417634aa3d812af327ffe9d620'

    Test wallets of PySeedRecover:
    >>> e = bytes.fromhex('7c7079e639eedf56920e134b606a49f8'
    ...                   '8ba21d42d0be517b8f29ecc6498c980b')
    >>> entropy2masterkey(e).hex()  # doctest: +NORMALIZE_WHITESPACE
    '00d370bf9e756fba12e7fa389a3551b97558b140267c88166136d4f0d2bea75c393f5e\
3e63e61578342fa8ab1313a7315693c5e679e3cf79f7fe8f13bf8ffe9c2a67ac173bbb2afd3\
4381905fa247c65c0d8eb66c42d2373d54bd5eef73e49da'
    >>> e = bytes.fromhex('7c7079e639eedf56920e134b606a49f8'
    ...                   '8ba21d42d0be517b8f29ecc6498c980f')
    >>> entropy2masterkey(e).hex()  # doctest: +NORMALIZE_WHITESPACE
    'b03595d980ab77fac0d95d0e563de43ad2978b2a22e8f0a14ad69a1964eddf5ed13ffc\
0e596edf974cb477cb08c5fc499efbaafa5103a2afa6094468759c1d1c694734296dd915dd1\
61df3703a3c1e0b4562fad0b67fdbf3fa7b819791cc5cac'
    """
    key = bytearray(hashlib.pbkdf2_hmac('sha512', b'', entropy, 4096, 96))
    key[0] &= 0b11111000
    key[31] &= 0b00011111
    key[31] |= 0b01000000
    return key


def masterkey2stakekey(masterkey: bytes) -> bytes:
    """Derive stake key from master key.

    """


def stakekey2bech32(stakekey: bytes) -> str:
    """Encode stake key in BECH32.

    """


def seed2stakekey(seed: Iterable[str], wordlist: Wordlist) -> str:
    """Derive stake key from seed phrase."""
    return entropy2masterkey(seed2entropy(seed, wordlist)).hex()
