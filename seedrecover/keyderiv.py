"""Cardano key derivation from seed phrases.

>>> wordlist = Wordlist()
"""
import hashlib

from seedrecover.wordlist import Wordlist

from typing import Iterable, Optional, Tuple


class ChecksumError(Exception):
    """Raised if checksum is not correct."""

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


BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32encode(readable: str, data: bytes) -> str:
    """Encode data with BECH32 using given human-readable part.

    Algorithm is described in:
    https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
    Reference implementation is given in:
    https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py

    >>> data = bytes([0b11100001])
    >>> data += bytes.fromhex('56fab56e0aed4f7b59ff25a1f08d'
    ...                       'f1d56d6a619a6945b461d358e98a')
    >>> bech32encode('stake', data)
    'stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq'
    >>> data = bytes([0b11100001])
    >>> data += bytes.fromhex('59b8841a4c7b4b919ca88ef9132b'
    ...                       'e58ee596cc6b3553f7477d4577b2')
    >>> bech32encode('stake', data)
    'stake1u9vm3pq6f3a5hyvu4z80jyetuk8wt9kvdv648a6804zh0vscalg0n'
    """
    # TODO Check readable for ASCII
    # TODO More tests from the BIP
    data_int5 = []
    bits = 0
    current = 0
    for byte in data:
        bits += 8
        current = (current << 8) + byte
        while bits >= 5:
            bits -= 5
            int5 = current >> bits
            data_int5.append(int5)
            current -= int5 << bits
    if bits:
        int5 = current << (5 - bits)
        data_int5.append(int5)
    to_check = [ord(char) >> 5 for char in readable] + [0]
    to_check += [ord(char) & 31 for char in readable]
    to_check += data_int5
    to_check += [0, 0, 0, 0, 0, 0]
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    checksum = 1
    for int5 in to_check:
        top = checksum >> 25
        checksum = (checksum & 0x1ffffff) << 5 ^ int5
        for i in range(5):
            checksum ^= generator[i] if ((top >> i) & 1) else 0
    checksum ^= 1
    data_int5 += [(checksum >> 5 * (5 - i)) & 31 for i in range(6)]
    bech32 = readable + '1'
    bech32 += ''.join([BECH32_CHARSET[int5] for int5 in data_int5])
    return bech32


def bech32decode(bech32: str) -> Tuple[str, bytes]:
    """Decode BECH32 string into human-readable part and data.

    Algorithm is described in:
    https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
    Reference implementation is given in:
    https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py

    >>> bech32 = 'stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq'
    >>> readable, data = bech32decode(bech32)
    >>> readable
    'stake'
    >>> bin(data[0])
    '0b11100001'
    >>> data[1:].hex()
    '56fab56e0aed4f7b59ff25a1f08df1d56d6a619a6945b461d358e98a'
    >>> bech32 = 'stake1u9vm3pq6f3a5hyvu4z80jyetuk8wt9kvdv648a6804zh0vscalg0n'
    >>> readable, data = bech32decode(bech32)
    >>> readable
    'stake'
    >>> bin(data[0])
    '0b11100001'
    >>> data[1:].hex()
    '59b8841a4c7b4b919ca88ef9132be58ee596cc6b3553f7477d4577b2'
    """
    # TODO Format checks: all lower xor all upper, all ASCII, ...
    # TODO More tests from the BIP
    readable, _, data_string = bech32.rpartition('1')
    data_int5 = [BECH32_CHARSET.find(char) for char in data_string.lower()]
    to_check = [ord(char) >> 5 for char in readable] + [0]
    to_check += [ord(char) & 31 for char in readable]
    to_check += data_int5
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    checksum = 1
    for int5 in to_check:
        top = checksum >> 25
        checksum = (checksum & 0x1ffffff) << 5 ^ int5
        for i in range(5):
            checksum ^= generator[i] if ((top >> i) & 1) else 0
    if checksum != 1:
        raise ChecksumError
    data = bytearray()
    bits = 0
    current = 0
    for int5 in data_int5[:-6]:
        bits += 5
        current = (current << 5) + int5
        while bits >= 8:
            bits -= 8
            byte = current >> bits
            data.append(byte)
            current -= byte << bits
    return readable, data


def generate_shelley_address(payment_key: Optional[bytes],
                             stake_key: Optional[bytes]) -> str:
    """Generate Cardano Shelley addresses from keys.

    Algorithm is defined in:
    https://github.com/cardano-foundation/CIPs/tree/master/CIP-0019

    >>> _, payment_key = bech32decode('addr_vk1w0l2sr2zgfm26ztc6nl9xy8gh'
    ...                               'sk5sh6ldwemlpmp9xylzy4dtf7st80zhd')
    >>> _, stake_key = bech32decode('stake_vk1px4j0r2fk7ux5p23shz8f3y5y'
    ...                             '2qam7s954rgf3lg5merqcj6aetsft99wu')
    >>> generate_shelley_address(payment_key,
    ...                          stake_key)  # doctest: +NORMALIZE_WHITESPACE
    'addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktc\
d8cc3sq835lu7drv2xwl2wywfgse35a3x'
    >>> generate_shelley_address(payment_key,
    ...                          None)  # doctest: +NORMALIZE_WHITESPACE
    'addr1vx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzers66hrl8'
    >>> generate_shelley_address(None,
    ...                          stake_key)  # doctest: +NORMALIZE_WHITESPACE
    'stake1uyehkck0lajq8gr28t9uxnuvgcqrc6070x3k9r8048z8y5gh6ffgw'
    >>> generate_shelley_address(None, None)
    Traceback (most recent call last):
        ...
    ValueError: At least one key required.
    """
    if payment_key is None:
        if stake_key is None:
            raise ValueError("At least one key required.")
        else:
            readable = 'stake'
            stake_hash = hashlib.blake2b(stake_key, digest_size=28)
            data = bytes([0b11100001])
            data += stake_hash.digest()
    else:
        readable = 'addr'
        payment_hash = hashlib.blake2b(payment_key, digest_size=28)
        if stake_key is None:
            data = bytes([0b01100001])
            data += payment_hash.digest()
        else:
            stake_hash = hashlib.blake2b(stake_key, digest_size=28)
            data = bytes([0b00000001])
            data += payment_hash.digest()
            data += stake_hash.digest()
    return bech32encode(readable, data)


def seed2stakeaddress(seed: Iterable[str], wordlist: Wordlist) -> str:
    """Derive stake key from seed phrase."""
    entropy = seed2entropy(seed, wordlist)
    master_key = entropy2masterkey(entropy)
    stake_key = masterkey2stakekey(master_key)
    stake_address = generate_shelley_address(None, stake_key)
    return stake_address
