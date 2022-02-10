"""Cardano key derivation from seed phrases.

The derivation of a stake address from a seed phrase is implemented step-wise
by first deriving an entropy from the seed phrase, deriving a master key from
the entropy, a stake key from the master key, and finally encoding the hash
of the stake key with BECH32.

The whole process is done by seed_to_stakeaddress:
>>> wordlist = Wordlist()
>>> seed_to_stakeaddress(["ladder", "long", "kangaroo", "inherit", "unknown",
...                       "prize", "else", "second", "enter", "addict",
...                       "mystery", "valve", "riot", "attitude", "area",
...                       "blind", "fabric", "symbol", "skill", "sunset",
...                       "goose", "shock", "gasp", "grape"], wordlist)
'stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq'
>>> seed_to_stakeaddress(["ladder", "long", "kangaroo", "inherit", "unknown",
...                       "prize", "else", "second", "enter", "addict",
...                       "mystery", "valve", "riot", "attitude", "area",
...                       "blind", "fabric", "symbol", "skill", "sunset",
...                       "goose", "shock", "gasp", "uphold"], wordlist)
'stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh'
"""
import ecpy.curves  # type: ignore
import hashlib
import hmac

from seedrecover.wordlist import Wordlist

from typing import Iterable, Optional, Tuple


class ChecksumError(Exception):
    """Raised if checksum is not correct."""

    pass


def seed_to_entropy(seed: Iterable[str], wordlist: Wordlist) -> bytes:
    """Derive entropy from seed phrase.

    Algorithm is specified in BIP-0039:
    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

    >>> wordlist = Wordlist()

    If the checksum is wrong, a ChecksumError is raised:
    >>> seed_to_entropy(["abandon", "abandon", "abandon", "abandon", "abandon",
    ...                  "abandon", "abandon", "abandon", "abandon", "abandon",
    ...                  "abandon", "abandon"], wordlist).hex()
    Traceback (most recent call last):
        ...
    keyderiv.ChecksumError

    Test vectors linked in BIP-0039:
    >>> seed_to_entropy(["abandon", "abandon", "abandon", "abandon", "abandon",
    ...                  "abandon", "abandon", "abandon", "abandon", "abandon",
    ...                  "abandon", "about"], wordlist).hex()
    '00000000000000000000000000000000'
    >>> seed_to_entropy(["legal", "winner", "thank", "year", "wave",
    ...                  "sausage", "worth", "useful", "legal", "winner",
    ...                  "thank", "yellow"], wordlist).hex()
    '7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f'
    >>> seed_to_entropy(["letter", "advice", "cage", "absurd", "amount",
    ...                  "doctor", "acoustic", "avoid", "letter", "advice",
    ...                  "cage", "above"], wordlist).hex()
    '80808080808080808080808080808080'
    >>> seed_to_entropy(["zoo", "zoo", "zoo", "zoo", "zoo",
    ...                  "zoo", "zoo", "zoo", "zoo", "zoo",
    ...                  "zoo", "wrong"], wordlist).hex()
    'ffffffffffffffffffffffffffffffff'

    Test vector for master key derivation (see entropy_to_masterkey):
    >>> seed_to_entropy(["eight", "country", "switch", "draw", "meat",
    ...                  "scout", "mystery", "blade", "tip", "drift",
    ...                  "useless", "good", "keep", "usage", "title"],
    ...                 wordlist).hex()
    '46e62370a138a182a498b8e2885bc032379ddf38'

    Test wallets of PySeedRecover:
    >>> seed_to_entropy(["ladder", "long", "kangaroo", "inherit", "unknown",
    ...                  "prize", "else", "second", "enter", "addict",
    ...                  "mystery", "valve", "riot", "attitude", "area",
    ...                  "blind", "fabric", "symbol", "skill", "sunset",
    ...                  "goose", "shock", "gasp", "grape"], wordlist).hex()
    '7c7079e639eedf56920e134b606a49f88ba21d42d0be517b8f29ecc6498c980b'
    >>> seed_to_entropy(["ladder", "long", "kangaroo", "inherit", "unknown",
    ...                  "prize", "else", "second", "enter", "addict",
    ...                  "mystery", "valve", "riot", "attitude", "area",
    ...                  "blind", "fabric", "symbol", "skill", "sunset",
    ...                  "goose", "shock", "gasp", "uphold"], wordlist).hex()
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


def entropy_to_masterkey(entropy: bytes) -> bytes:
    """Derive master key from entropy.

    Algorithm is specified in:
    https://github.com/cardano-foundation/CIPs/blob/master/CIP-0003/Icarus.md

    Test vector from CIP-0003:
    >>> e = bytes.fromhex('46e62370a138a182a498b8e2885bc032379ddf38')
    >>> entropy_to_masterkey(e).hex()
    'c065afd2832cd8b087c4d9ab7011f481ee1e0721e78ea5dd609f3ab3f156d245d176bd\
8fd4ec60b4731c3918a2a72a0226c0cd119ec35b47e4d55884667f552a23f7fdcd4a10c6cd2\
c7393ac61d877873e248f417634aa3d812af327ffe9d620'

    Test wallets of PySeedRecover:
    >>> e = bytes.fromhex('7c7079e639eedf56920e134b606a49f8'
    ...                   '8ba21d42d0be517b8f29ecc6498c980b')
    >>> entropy_to_masterkey(e).hex()
    '00d370bf9e756fba12e7fa389a3551b97558b140267c88166136d4f0d2bea75c393f5e\
3e63e61578342fa8ab1313a7315693c5e679e3cf79f7fe8f13bf8ffe9c2a67ac173bbb2afd3\
4381905fa247c65c0d8eb66c42d2373d54bd5eef73e49da'
    >>> e = bytes.fromhex('7c7079e639eedf56920e134b606a49f8'
    ...                   '8ba21d42d0be517b8f29ecc6498c980f')
    >>> entropy_to_masterkey(e).hex()
    'b03595d980ab77fac0d95d0e563de43ad2978b2a22e8f0a14ad69a1964eddf5ed13ffc\
0e596edf974cb477cb08c5fc499efbaafa5103a2afa6094468759c1d1c694734296dd915dd1\
61df3703a3c1e0b4562fad0b67fdbf3fa7b819791cc5cac'
    """
    key = bytearray(hashlib.pbkdf2_hmac('sha512', b'', entropy, 4096, 96))
    key[0] &= 0b11111000
    key[31] &= 0b00011111
    key[31] |= 0b01000000
    return key


ed25519 = ecpy.curves.Curve.get_curve("Ed25519")
ed25519_n = 2**252 + 27742317777372353535851937790883648493


def masterkey_to_rootkey(masterkey: bytes) -> Tuple[bytes, bytes, bytes]:
    """Decompose masterkey and compute public key.

    Decomposition of masterkey into k and c is given in:
    https://github.com/cardano-foundation/CIPs/tree/master/CIP-0003
    Derivation of A according to:
    https://doi.org/10.1109/EuroSPW.2017.47
    """
    c = masterkey[64:]
    k = masterkey[:64]
    k_L = int.from_bytes(k[:32], 'little')
    A = ed25519.encode_point(k_L * ed25519.generator)
    return k, A, c


def child_key(k_parent: bytes, A_parent: bytes, c_parent: bytes,
              i: int) -> Tuple[bytes, bytes, bytes]:
    """Derive child key from parent key.

    Algorithm specified in:
    https://doi.org/10.1109/EuroSPW.2017.47
    Example implementation in:
    https://github.com/LedgerHQ/orakolo/blob/master/src/python/orakolo/HDEd25519.py
    """
    index = i.to_bytes(4, 'little')
    if i < 2**31:
        Z = hmac.new(c_parent, b'\x02' + A_parent + index,
                     hashlib.sha512).digest()
        c = hmac.new(c_parent, b'\x03' + A_parent + index,
                     hashlib.sha512).digest()[32:]
    else:
        Z = hmac.new(c_parent, b'\x00' + k_parent + index,
                     hashlib.sha512).digest()
        c = hmac.new(c_parent, b'\x01' + k_parent + index,
                     hashlib.sha512).digest()[32:]
    k_L = int.from_bytes(Z[:28], 'little') * 8
    k_L += int.from_bytes(k_parent[:32], 'little')
    if k_L % ed25519_n == 0:
        raise ValueError("k_L is zero.")
    k_R = int.from_bytes(Z[32:], 'little')
    k_R += int.from_bytes(k_parent[32:], 'little')
    k_R %= 2**256
    k = k_L.to_bytes(32, 'little') + k_R.to_bytes(32, 'little')
    A = ed25519.encode_point(k_L * ed25519.generator)
    return k, A, c


def masterkey_to_pubkey(masterkey: bytes, path: str) -> bytes:
    """Derive stake key from master key.

    Test wallets of PySeedRecover:
    >>> m = bytes.fromhex('00d370bf9e756fba12e7fa389a3551b97558b140267c8816'
    ...                   '6136d4f0d2bea75c393f5e3e63e61578342fa8ab1313a731'
    ...                   '5693c5e679e3cf79f7fe8f13bf8ffe9c2a67ac173bbb2afd'
    ...                   '34381905fa247c65c0d8eb66c42d2373d54bd5eef73e49da')
    >>> masterkey_to_pubkey(m, "1852'/1815'/0'/2/0").hex()
    '71bf7bfed46252ab6080e19391521a7af962b2b85f1a75c5e75ec0da7d665c99'
    >>> m = bytes.fromhex('b03595d980ab77fac0d95d0e563de43ad2978b2a22e8f0a1'
    ...                   '4ad69a1964eddf5ed13ffc0e596edf974cb477cb08c5fc49'
    ...                   '9efbaafa5103a2afa6094468759c1d1c694734296dd915dd'
    ...                   '161df3703a3c1e0b4562fad0b67fdbf3fa7b819791cc5cac')
    >>> masterkey_to_pubkey(m, "1852'/1815'/0'/2/0").hex()
    '9ec748e483ae666c99aaae21434f6c5f77bf40c3b44ea68a0eb6f48617a5aa9e'
    """
    k, A, c = masterkey_to_rootkey(masterkey)
    for component in path.split('/'):
        if component.endswith("'"):
            index = int(component[:-1]) + 2**31
        else:
            index = int(component)
        k, A, c = child_key(k, A, c, index)
    return A


class BECH32FormatError(Exception):
    """Raised if a requirement for BECH32 is not fulfilled."""

    pass


BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32_GENERATOR = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]


def bech32_encode(readable: str, data: bytes) -> str:
    """Encode data with BECH32 using given human-readable part.

    Algorithm is specified in:
    https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
    Reference implementation is given in:
    https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py

    Valid test vectors from BIP-0173:
    >>> bech32_encode('a', b'')
    'a12uel5l'
    >>> bech32_encode('abcdef', bytes.fromhex('00443214c74254b635cf'
    ...                                       '84653a56d7c675be77df'))
    'abcdef1qpzry9x8gf2tvdw0s3jn54khce6mua7lmqqqxw'
    >>> bech32_encode('split', bytes.fromhex('c5f38b70305f519bf66d85fb6cf030'
    ...                                      '58f3dde463ecd7918f2dc743918f2d'))
    'split1checkupstagehandshakeupstreamerranterredcaperred2y9e3w'

    Invalid test vectors from BIP-0173:
    >>> bech32_encode('', b'')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Readable part is empty.
    >>> bech32_encode(chr(0x20), b'')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in readable part.
    >>> bech32_encode(chr(0x7F), b'')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in readable part.
    >>> bech32_encode(chr(0x80), b'')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in readable part.

    Test wallets of PySeedRecover:
    >>> data = bytes([0b11100001])
    >>> data += bytes.fromhex('56fab56e0aed4f7b59ff25a1f08d'
    ...                       'f1d56d6a619a6945b461d358e98a')
    >>> bech32_encode('stake', data)
    'stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq'
    >>> data = bytes([0b11100001])
    >>> data += bytes.fromhex('c3a379f52b9f411c8a701c91b4cf'
    ...                       'ab45c08ac4ce8e0b30a2c67116b8')
    >>> bech32_encode('stake', data)
    'stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh'
    """
    # Check format of human-readable part:
    if not readable:
        raise BECH32FormatError("Readable part is empty.")
    if any(ord(char) < 33 or ord(char) > 126 for char in readable):
        raise BECH32FormatError("Invalid character in readable part.")
    # Recode bytes into 5-bit integers:
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
    # Calculate checksum:
    to_check = [ord(char) >> 5 for char in readable] + [0]
    to_check += [ord(char) & 31 for char in readable]
    to_check += data_int5
    to_check += [0, 0, 0, 0, 0, 0]
    checksum = 1
    for int5 in to_check:
        top = checksum >> 25
        checksum = (checksum & 0x1ffffff) << 5 ^ int5
        for i in range(5):
            checksum ^= BECH32_GENERATOR[i] if ((top >> i) & 1) else 0
    checksum ^= 1
    # Compose and encode 5-bit integers into characters:
    data_int5 += [(checksum >> 5 * (5 - i)) & 31 for i in range(6)]
    bech32 = readable + '1'
    bech32 += ''.join([BECH32_CHARSET[int5] for int5 in data_int5])
    return bech32


def bech32_decode(bech32: str) -> Tuple[str, bytes]:
    """Decode BECH32 string into human-readable part and data.

    Algorithm is specified in:
    https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
    Reference implementation is given in:
    https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py

    Valid test vectors from BIP-0173:
    >>> readable, data = bech32_decode('A12UEL5L')
    >>> readable
    'a'
    >>> data.hex()
    ''
    >>> readable, data = bech32_decode('a12uel5l')
    >>> readable
    'a'
    >>> data.hex()
    ''
    >>> readable, data = bech32_decode('an83characterlonghumanreadable'
    ...                                'partthatcontainsthenumber1and'
    ...                                'theexcludedcharactersbio1tt5tgs')
    >>> readable
    'an83characterlonghumanreadablepartthatcontainsthenumber1andtheexcluded\
charactersbio'
    >>> data.hex()
    ''
    >>> readable, data = bech32_decode('abcdef1qpzry9x8gf2tvdw0'
    ...                                's3jn54khce6mua7lmqqqxw')
    >>> readable
    'abcdef'
    >>> data.hex()
    '00443214c74254b635cf84653a56d7c675be77df'
    >>> readable, data = bech32_decode('11qqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    ...                                'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    ...                                'qqqqqqqqqqqqqqqqqqqqqqqqc8247j')
    >>> readable
    '1'
    >>> data.hex()
    '0000000000000000000000000000000000000000000000000000000000000000000000\
00000000000000000000000000000000'
    >>> readable, data = bech32_decode('split1checkupstagehandshakeupstream'
    ...                                'erranterredcaperred2y9e3w')
    >>> readable
    'split'
    >>> data.hex()
    'c5f38b70305f519bf66d85fb6cf03058f3dde463ecd7918f2dc743918f2d'
    >>> readable, data = bech32_decode('?1ezyfcl')
    >>> readable
    '?'
    >>> data.hex()
    ''

    Invalid mix of uppercase and lowercase:
    >>> readable, data = bech32_decode('aBcDeF1qPzRy9x8gF2TvDw0'
    ...                                's3jN54KhCe6mUa7lMqQqXw')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: BECH32 string mixes uppercase and lowercase.

    Invalid test vectors from BIP-0173:
    >>> readable, data = bech32_decode(chr(0x20) + '1nwldj5')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in readable part.
    >>> readable, data = bech32_decode(chr(0x7F) + '1axkwrx')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in readable part.
    >>> readable, data = bech32_decode(chr(0x80) + '1eym55h')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in readable part.
    >>> readable, data = bech32_decode('pzry9x0s0muk')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: BECH32 string has no separator ('1').
    >>> readable, data = bech32_decode('1pzry9x0s0muk')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Readable part is empty.
    >>> readable, data = bech32_decode('x1b4n0q5v')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in data part.
    >>> readable, data = bech32_decode('li1dgmt3')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Data part is too short.
    >>> readable, data = bech32_decode('de1lg7wt' + chr(0xFF))
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Invalid character in data part.
    >>> readable, data = bech32_decode('A1G7SGD8')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Checksum of BECH32 string does not match.
    >>> readable, data = bech32_decode('10a06t8')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Readable part is empty.
    >>> readable, data = bech32_decode('1qzzfhee')
    Traceback (most recent call last):
        ...
    keyderiv.BECH32FormatError: Readable part is empty.

    Test wallets of PySeedRecover:
    >>> bech32 = 'stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq'
    >>> readable, data = bech32_decode(bech32)
    >>> readable
    'stake'
    >>> bin(data[0])
    '0b11100001'
    >>> data[1:].hex()
    '56fab56e0aed4f7b59ff25a1f08df1d56d6a619a6945b461d358e98a'
    >>> bech32 = 'stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh'
    >>> readable, data = bech32_decode(bech32)
    >>> readable
    'stake'
    >>> bin(data[0])
    '0b11100001'
    >>> data[1:].hex()
    'c3a379f52b9f411c8a701c91b4cfab45c08ac4ce8e0b30a2c67116b8'
    """
    # Check format, divide human-readable and data part
    # and decode characters to 5-bit integers:
    if not bech32 == bech32.lower() and not bech32 == bech32.upper():
        raise BECH32FormatError("BECH32 string mixes uppercase and lowercase.")
    bech32 = bech32.lower()
    if '1' not in bech32:
        raise BECH32FormatError("BECH32 string has no separator ('1').")
    readable, _, data_string = bech32.rpartition('1')
    if not readable:
        raise BECH32FormatError("Readable part is empty.")
    if any(ord(char) < 33 or ord(char) > 126 for char in readable):
        raise BECH32FormatError("Invalid character in readable part.")
    if len(data_string) < 6:
        raise BECH32FormatError("Data part is too short.")
    if any(char not in BECH32_CHARSET for char in data_string):
        raise BECH32FormatError("Invalid character in data part.")
    data_int5 = [BECH32_CHARSET.find(char) for char in data_string]
    # Calculate checksum:
    to_check = [ord(char) >> 5 for char in readable] + [0]
    to_check += [ord(char) & 31 for char in readable]
    to_check += data_int5
    checksum = 1
    for int5 in to_check:
        top = checksum >> 25
        checksum = (checksum & 0x1ffffff) << 5 ^ int5
        for i in range(5):
            checksum ^= BECH32_GENERATOR[i] if ((top >> i) & 1) else 0
    if checksum != 1:
        raise BECH32FormatError("Checksum of BECH32 string does not match.")
    # Recode 5-bit integers into bytes:
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

    Algorithm is specified in:
    https://github.com/cardano-foundation/CIPs/tree/master/CIP-0019

    Test vectors of CIP-0019:
    >>> _, payment_key = bech32_decode('addr_vk1w0l2sr2zgfm26ztc6nl9xy8gh'
    ...                                'sk5sh6ldwemlpmp9xylzy4dtf7st80zhd')
    >>> _, stake_key = bech32_decode('stake_vk1px4j0r2fk7ux5p23shz8f3y5y'
    ...                              '2qam7s954rgf3lg5merqcj6aetsft99wu')
    >>> generate_shelley_address(payment_key, stake_key)
    'addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktc\
d8cc3sq835lu7drv2xwl2wywfgse35a3x'
    >>> generate_shelley_address(payment_key, None)
    'addr1vx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzers66hrl8'
    >>> generate_shelley_address(None, stake_key)
    'stake1uyehkck0lajq8gr28t9uxnuvgcqrc6070x3k9r8048z8y5gh6ffgw'
    >>> generate_shelley_address(None, None)
    Traceback (most recent call last):
        ...
    ValueError: At least one key required.

    Test wallets of PySeedRecover:
    >>> stake_key = bytes.fromhex('71bf7bfed46252ab6080e19391521a7a'
    ...                           'f962b2b85f1a75c5e75ec0da7d665c99')
    >>> generate_shelley_address(None,
    ...                          stake_key)
    'stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq'
    >>> stake_key = bytes.fromhex('9ec748e483ae666c99aaae21434f6c5f'
    ...                           '77bf40c3b44ea68a0eb6f48617a5aa9e')
    >>> generate_shelley_address(None,
    ...                          stake_key)
    'stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh'
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
    return bech32_encode(readable, data)


def seed_to_stakeaddress(seed: Iterable[str], wordlist: Wordlist) -> str:
    """Derive stake key from seed phrase."""
    entropy = seed_to_entropy(seed, wordlist)
    master_key = entropy_to_masterkey(entropy)
    stake_key = masterkey_to_pubkey(master_key, "1852'/1815'/0'/2/0")
    stake_address = generate_shelley_address(None, stake_key)
    return stake_address
