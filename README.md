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
                        check on blockfrost
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
