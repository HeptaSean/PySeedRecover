"""Test for given stake addresses.

An instance of the StakeAddresses class is initialised with a list of stake
addresses to search for. The check_stake_address method then checks given
stake addresses against this list:
>>> addresses = ["stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq",
...              "stake1u9vm3pq6f3a5hyvu4z80jyetuk8wt9kvdv648a6804zh0vscalg0n"]
>>> sk = StakeAddresses(addresses)
>>> existing = "stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq"
>>> missing = "stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh"
>>> sk.check_stake_address(existing)
True
>>> sk.check_stake_address(missing)
False

The searched stake addresses in the initial list can contain omissions marked
by three dots:
>>> addresses = ["stake1u9...24r8yq", "stake1u9...calg0n"]
>>> sk = StakeAddresses(addresses)
>>> sk.check_stake_address(existing)
True
>>> sk.check_stake_address(missing)
False
"""
import re

from typing import Iterable


class StakeAddresses:
    """Test stake addresses against list of searched addresses."""

    def __init__(self, addresses: Iterable[str]) -> None:
        """Initialise list of searched addresses."""
        self._patterns = []
        for a in addresses:
            expr = re.compile(a.replace('...', '.*'))
            self._patterns.append(expr)

    def check_stake_address(self, stake_address: str) -> bool:
        """Check if the stake address is in the list."""
        for pattern in self._patterns:
            if pattern.fullmatch(stake_address):
                return True
        return False
