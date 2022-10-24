"""Recover Cardano seed phrases.

Contains the following modules:
- __main__.py: Execute the command-line interface as __main__.
- cli.py: Command line interface including input and output.
- wordlist.py: Wordlist for BIP-39.
- order.py: Permutations, combinations, and extensions of given lists.
- keyderiv.py: Cardano key derivation from seed phrases.
- stakecheck.py: Test for given stake addresses.
- koios.py: Test for active stake addresses through koios.rest.

Roadmap:
2.0.0
TODO koios.py: Asynchronous query of stake addresses in bulks
TODO stakecheck.py: Allow base address and extract stake address
TODO stakecheck.py: Check for plausible structure of given addresses
TODO stakecheck.py: Check against bytes to avoid Bech32 overhead
TODO cli.py: Mark positions instead of -m parameter
2.1.0
TODO order.py: Start with reorder in the middle
TODO order.py: Add exchange of adjacent positions to reorder?
TODO order.py: Avoid repetitions of same seed phrases
TODO order.py: Less modifications first
3.0.0
TODO Base on Gerolamo library of CIP/BIP/... implementations
TODO Byron, Ledger, and Trezor support
TODO Multi-account support
"""
__version__ = "1.9.0"
