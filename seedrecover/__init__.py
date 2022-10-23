"""Package seedrecover of project PySeedRecover.

Contains the following modules:
- __main__.py: Execute the command-line interface as __main__.
- cli.py: Command line interface including input and output.
- wordlist.py: Wordlist for BIP-39.
- order.py: Permutations, combinations, and extensions of given lists.
- keyderiv.py: Cardano key derivation from seed phrases.
- stakecheck.py: Test for given stake addresses.
- koios.py: Test for active stake addresses through koios.rest.

TODO order.py: Start with reorder in the middle
TODO order.py: Add exchange of adjacent positions to reorder?
TODO stakecheck.py: Check for plausible structure of given addresses
TODO stakecheck.py: Allow base address and extract stake address
TODO koios.py: Asynchronous query of stake addresses in bulks
TODO order.py: Avoid repetitions of same seed phrases
TODO Byron, Ledger, and Trezor support
TODO Multi-account support
"""
