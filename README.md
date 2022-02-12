# PySeedRecover
This is a Python script to recover a
[BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
mnemonic seed phrase if words are missing, were written down in a wrong or
unknown order, or there is a typo in them, especially when used on the
Cardano crypto currency network.

This script will probably *not* help you, when you get an empty wallet
after restoring/importing with a seed phrase.
Since seed phrases contain a checksum, it is very unlikely to get to
another valid seed phrase (that opens an empty wallet) by wrong orders or
typos.
Empty wallets rather indicate that the restored/imported seed phrase is the
wrong one altogether – saved from a trial that was never really used or
something like that.

## Crypto Currency Disclaimer
I do not endorse the use of crypto currencies or the ecosystems built around
them, right now.
Proof-of-work networks like Bitcoin and Ethereum are ecologically harmful
on an unprecedented scale.
Proof-of-stake networks like Cardano do not have *that* problem, but still
have to prove their utility for real use cases.

Do *not* invest money that you cannot afford to *completely* lose into
crypto currencies (let alone NFTs and other strange tokens without any real
value)!
Their future is totally unclear.

The technology behind them is interesting, though.
And this script does explore a part of this technology (and hopefully helps
some people get their wallets back).

## Installation
You need a working Python 3 installation on your machine.
I do development on the newest stable version (3.10), but test it also on
the oldest
[still supported](https://devguide.python.org/#status-of-python-branches)
version (3.7).

Installation instructions for Windows can be found at:
[https://docs.microsoft.com/en-us/windows/python/beginners](https://docs.microsoft.com/en-us/windows/python/beginners)
(That guide links to Python 3.7, Python 3.10 can be found at
[https://www.microsoft.com/de-de/p/python-310/9pjpw5ldxlz5](https://www.microsoft.com/de-de/p/python-310/9pjpw5ldxlz5).)

For APT-based Linux distributions `apt install python3 python3-pip` should
be enough and for Arch-based Linux distributions `pacman -S python
python-pip` will install everything that is needed.

This script is then installed by `pip install PySeedRecover` (or `pip3
install PySeedRecover` if the standard Python on your operating system is
still Python 2).

After that, `seedrecover -h` should show you the usage information of the
script.

## Usage
```
usage: seedrecover [-h] [-w FILE] [-s EDIT DISTANCE] [-o]
                   [-l LENGTH] [-m POSITION [POSITION ...]]
                   [-a ADDRESS [ADDRESS ...]] [-b API KEY]
                   [WORD ...]

positional arguments:
  WORD                  known words of seed phrase

options:
  -h, --help            show this help message and exit
  -w FILE, --wordlist FILE
                        wordlist to use (default: english)
  -s EDIT DISTANCE, --similar EDIT DISTANCE
                        try similar words up to edit distance
  -o, --order           try different orders of seed words
  -l LENGTH, --length LENGTH
                        length of seed phrase
  -m POSITION [POSITION ...], --missing POSITION [POSITION ...]
                        missing word positions
  -a ADDRESS [ADDRESS ...], --address ADDRESS [ADDRESS ...]
                        check for stake addresses
  -b API KEY, --blockfrost API KEY
                        check on BlockFrost
```
> **WARNING:** If you give your (partial knowledge of your) seed phrase to
> this script on the command line, this information will be in the history
> of the shell you are using.
> It is also visible on screen and can perhaps be scrolled back.
> For security, clear the history and close the terminal after using this
> script.

We are using a test wallet that I generated with the following seed phrase:
```
ladder   long     kangaroo inherit  unknown  prize
else     second   enter    addict   mystery  valve
riot     attitude area     blind    fabric   symbol
skill    sunset   goose    shock    gasp     grape
```
The stake address for this test wallet is
`stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq`.

The simplest way to get something wrong are just small typos, some of which
may lead to other valid words, some of which not.
If we suspect that we did that, we can choose with the `-s`/`--similar`
option, up to which edit distance we want to search for valid seed phrases:
```
$ seedrecover -s 1 ladder long kangaroo inherit unknown price else second \
  enter addict mystery valve riot altitude area blind fabric symbol skill \
  sunset goose shock gap grape
ladder => ladder
long => long, song
kangaroo => kangaroo
inherit => inherit
unknown => unknown
price => price, pride, prize, rice
else => else
second => second
enter => enter
addict => addict
mystery => mystery
valve => valve
riot => riot
'altitude' not in wordlist!
altitude => attitude
area => area, arena
blind => bind, blind
fabric => fabric
symbol => symbol
skill => skill, skull, still
sunset => sunset
goose => goose
shock => shock, sock, stock
gap => gap, gas, gasp
grape => grace, grape
Length not set. Using smallest length for given phrase.
0 of 24 words missing.
Seed phrases checked:          6 total,          1 fulfilled checksum,          1 without repetitions
stake1uy5gjrvr3kql0t8j4vsn99w6y4h8zc95e22m4edjjg894kcg644qn: ladder long kangaroo inherit unknown price else second enter addict mystery valve riot attitude area bind fabric symbol skill sunset goose shock gasp grape
[…]
Seed phrases checked:        492 total,          3 fulfilled checksum,          3 without repetitions
stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq: ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp grape
[…]
Seed phrases checked:      1_728 total,          8 fulfilled checksum,          8 without repetitions
```
`seedrecover` first reports, which words are gonna be checked for the given
words (due to `-s` and to words missing in the wordlist).
It then tells us, which total seed words length it is considering and how
many words are missing.
During the checking phase, progress and found stake addresses with their
seed phrases are reported.

If a word is missing from your seed phrase and you know, at which position
it is missing, you can give the position (or several possible positions)
with the `-m`/`--missing` option (as usual on Unix systems, the list of
options can be terminated with `--` to stop the list of positions and start
the list of known words of the seed phrase):
```
$ seedrecover -m 1 24 -- ladder long kangaroo inherit unknown prize else \
  second enter addict mystery valve riot attitude area blind fabric symbol \
  skill sunset goose shock gasp
ladder => ladder
[…]
gasp => gasp
Length not set. Using smallest length for given phrase.
1 of 24 words missing.
Seed phrases checked:        155 total,          1 fulfilled checksum,          1 without repetitions
stake1uy23h76c4pad8hpluvhrfzvx5ll837epvppprk6wfazvjmcu9j0fn: battle ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp
[…]
Seed phrases checked:      2_863 total,         12 fulfilled checksum,         12 without repetitions
stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq: ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp grape
[…]
Seed phrases checked:      4_096 total,         16 fulfilled checksum,         16 without repetitions
```

If you do not know, at which position a word is missing (or if several
words are missing), the possibilities become too many to manually check.
With `-a`/`--address`, we can give one or several stake addresses to search
for:
```
$ seedrecover -a stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq \
  stake1u9vm3pq6f3a5hyvu4z80jyetuk8wt9kvdv648a6804zh0vscalg0n -- ladder long \
  kangaroo inherit unknown prize else second enter mystery valve riot \
  attitude area blind fabric symbol skill sunset goose shock gasp grape
ladder => ladder
[...]
enter => enter
mystery => mystery
[...]
grape => grape
Length not set. Using smallest length for given phrase.
1 of 24 words missing.
Seed phrases checked:     18_459 total,         74 fulfilled checksum,         74 without repetitions
Searched stake address found:
stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq: ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp grape
Seed phrases checked:     49_152 total,        195 fulfilled checksum,        195 without repetitions
```
This check already takes almost a minute, but it only gives us the searched
stake address and its seed phrase.
> **Note:** It is a good idea to give the stake addresses of all your
> wallets and accounts to `-a`.
> You never know if you mixed up the seed phrases and the one you are
> currently looking at is maybe for a different wallet than you think.

It is also possible to abbreviate the searched stake address(es) by `...` in
the middle:
```
$ seedrecover -a stake1u9...24r8yq stake1u9...calg0n -- ladder long \
  kangaroo inherit unknown prize else second enter mystery valve riot \
  attitude area blind fabric symbol skill sunset goose shock gasp grape
ladder => ladder
[...]
enter => enter
mystery => mystery
[...]
grape => grape
Length not set. Using smallest length for given phrase.
1 of 24 words missing.
Seed phrases checked:     18_459 total,         74 fulfilled checksum,         74 without repetitions
Searched stake address found:
stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq: ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp grape
Seed phrases checked:     49_152 total,        195 fulfilled checksum,        195 without repetitions
```

If the searched stake address is unknown, the stake addresses can be checked
via [BlockFrost](https://blockfrost.io/) for previous activity.
For this, an API key has to be given with the `-b`/`--blockfrost` option
(can be obtained on the given website):
```
$ seedrecover -b mainnetABCDEFGHIJKLMNOPQRZ -- ladder long kangaroo inherit \
  unknown prize else second enter mystery valve riot attitude area blind \
  fabric symbol skill sunset goose shock gasp grape
ladder => ladder
[...]
enter => enter
mystery => mystery
[...]
grape => grape
Length not set. Using smallest length for given phrase.
1 of 24 words missing.
Seed phrases checked:     18_459 total,         74 fulfilled checksum,         74 without repetitions
Active stake address found:
stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq: ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp grape
Seed phrases checked:     49_152 total,        195 fulfilled checksum,        195 without repetitions
```
In this case, 195 requests to BlockFrost were made.
This number will be much higher with more missing words or in combination
with other checks.
Remember that there is a limit of 50 000 requests in the free tier.

If you are unsure about the order, the `-o`/`--order` option allows to check
certain plausible reorderings (exchanges of rows and columns in a rectangular
notation of the seed phrase):
```
$ seedrecover -o -a stake1u9...24r8yq stake1u9...calg0n -- ladder else riot \
  skill long second attitude sunset kangaroo enter area goose inherit \
  addict blind shock unknown mystery fabric gasp prize valve symbol grape
ladder => ladder
[...]
grape => grape
Length not set. Using smallest length for given phrase.
0 of 24 words missing.
Seed phrases checked:          4 total,          1 fulfilled checksum,          1 without repetitions
Searched stake address found:
stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq: ladder long kangaroo inherit unknown prize else second enter addict mystery valve riot attitude area blind fabric symbol skill sunset goose shock gasp grape
Seed phrases checked:         23 total,          1 fulfilled checksum,          1 without repetitions
```
A check of all 24! = 6.2×10^23 permutations (for the 24 word seed phrase
case) is not feasible.

When combining the options (typos, missing worders, order), the number of
possible seed phrases explodes pretty quickly.
It will not be possible to check them on BlockFrost due to the request
limits and the search for stake address can take hours or even days.

## Development
To set up a development environment for this project, just clone it, create
a virtual environment and install it with `pip` in editable mode.
```
$ git clone https://github.com/HeptaSean/PySeedRecover.git
$ cd PySeedRecover
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U pip setuptools wheel
$ pip install -e .[dev]
```

I am using `pydocstyle`, `pycodestyle` and `mypy` to lint my code and
`doctest` to test it with tests embedded in the docstrings.
The script `lint.sh` in the root of the project runs them all for
individual modules.
```
$ ./lint.sh seedrecover/<module>.py
```

The test with Python 3.7 is done using `pyenv`.
```
$ pyenv install --list
$ pyenv install 3.7.12
$ PYENV_VERSION="3.7.12" python -m venv /tmp/venv
$ source /tmp/venv/bin/activate
$ pip install -U pip setuptools wheel
$ pip install .[dev]
$ ./lint.sh seedrecover/<module>.py (for all modules)
$ (test invocations from README.md)
```

Upload to PyPI is done with `twine`, which is also installed by the `[dev]`
option.
```
$ python setup.py sdist
$ twine upload -r testpypi dist/PySeedRecover-<Version>.tar.gz
$ twine upload dist/PySeedRecover-<Version>.tar.gz
```
