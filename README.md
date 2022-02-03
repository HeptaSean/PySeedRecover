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
This rather indicates that the restored/imported seed phrase is the wrong
one altogether – saved from a trial that was never really used or something
like that.

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
Installation instructions for Windows can be found at:
[https://docs.microsoft.com/en-us/windows/python/beginners](https://docs.microsoft.com/en-us/windows/python/beginners)
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
                   [-k STAKE KEY [STAKE KEY ...]] [-b API KEY]
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
  -k STAKE KEY [STAKE KEY ...], --key STAKE KEY [STAKE KEY ...]
                        check for stake keys
  -b API KEY, --blockfrost API KEY
                        check on BlockFrost
```

We are using a test wallet that I generated with the following seed phrase:
```
ladder   long     kangaroo inherit  unknown  prize
else     second   enter    addict   mystery  valve
riot     attitude area     blind    fabric   symbol
skill    sunset   goose    shock    gasp     grape
```
The stake key for this test wallet is
`stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq`.

The simplest way to get something wrong are just small typos, some of which
may lead to other valid words, some of which not.
If we suspect that we did that, we can choose with the `-s`/`--similar`
option, up to which edit distance we want to search for valid seed phrases:
```shell
$ seedrecover -s 1 ladder long kangaroo inherit unknown price else second \
  enter addict mystery valve riot altitude area blind fabric symbol skill \
  sunset goose shock gap grape
```

If a word is missing from your seed phrase and you know, at which position
it is missing, you can give the position (or several possible positions)
with the `-m`/`--missing` option:
```shell
$ seedrecover -m 1 24 ladder long kangaroo inherit unknown prize else \
  second enter addict mystery valve riot attitude area blind fabric symbol \
  skill sunset goose shock gasp
```

If you do not know, at which position a word is missing (or if several
words are missing), the possibilities become too many to manually check.
With `-k`/`--key`, we can give one or several stake keys to search for
(as usual on Unix systems, the list of options can be terminated with `--`
to start with the known words of the seed phrase):
```shell
$ seedrecover -k stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq \
  stake1u9vm3pq6f3a5hyvu4z80jyetuk8wt9kvdv648a6804zh0vscalg0n -- ladder long \
  kangaroo inherit unknown prize else second enter mystery valve riot \
  attitude area blind fabric symbol skill sunset goose shock gasp grape
```

It is also possible to abbreviate the searched stake key(s) by `...` in the
middle:
```shell
$ seedrecover -k stake1u9...24r8yq stake1u9...calg0n -- ladder long \
  kangaroo inherit unknown prize else second enter mystery valve riot \
  attitude area blind fabric symbol skill sunset goose shock gasp grape
```

If you are unsure about the order (for example, exchanged rows and
columns), the `-o`/`--order` option allows to check all permutations of the
given words (leading to many, many phrases to check):
```shell
$ seedrecover -k stake1u9...24r8yq stake1u9...calg0n -o ladder else riot \
  skill long second attitude sunset kangaroo enter area goose inherit \
  addict blind shock unknown mystery fabric gasp prize valve symbol grape
```

If the searched stake key is unknown, the stake keys can be checked via
[blockfrost.io](https://blockfrost.io/) for previous activity.
For this, an API key has to be given with the `-b`/`--blockfrost` option
(can be obtained on the given website):
```shell
$ seedrecover -b mainnetABCDEFGHIJKLMNOPQRSTUVWXYZ -o ladder else riot \
  skill long second attitude sunset kangaroo enter area goose inherit \
  addict blind shock unknown mystery fabric gasp prize valve symbol grape
```

So, if we do not have any idea, what is wrong with the seed phrase, we can
combine all these possibilities:
```shell
$ time seedrecover -s 1 -o -b mainnetABCDEFGHIJKLMNOPQRSTUVWXYZ ladder else \
  riot skill long second altitude sunset kangaroo enter area goose inherit \
  blind shock unknown mystery fabric gap price valve symbol grape
```

## Development
To set up a development environment for this project:
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
individual modules: `./lint.sh seedrecover/<module>.py`
