"""Test for given stake keys.

An instance of the StakeKeys class is initialised with a list of stake keys
to search for. The check_stake_key method then checks given stake keys
against this list:
>>> keys = ["stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq",
...         "stake1u9vm3pq6f3a5hyvu4z80jyetuk8wt9kvdv648a6804zh0vscalg0n"]
>>> sk = StakeKeys(keys)
>>> existing = "stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq"
>>> missing = "stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh"
>>> sk.check_stake_key(existing)
True
>>> sk.check_stake_key(missing)
False

The searched stake keys in the initial list can contain omissions marked by
three dots:
>>> keys = ["stake1u9...24r8yq", "stake1u9...calg0n"]
>>> sk = StakeKeys(keys)
>>> sk.check_stake_key(existing)
True
>>> sk.check_stake_key(missing)
False
"""
import re


class StakeKeys:
    """Test stake keys against list of searched keys."""

    def __init__(self, keys: list[str]) -> None:
        """Initialise list of searched keys."""
        self._patterns = []
        for k in keys:
            expr = re.compile(k.replace('...', '.*'))
            self._patterns.append(expr)

    def check_stake_key(self, stake_key: str) -> bool:
        """Check if the stake key is in the list."""
        for pattern in self._patterns:
            if pattern.fullmatch(stake_key):
                return True
        return False
