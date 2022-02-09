"""Test for active stake addresses through BlockFrost API.

In order to use the BlockFrost API, an API key is needed that can be
obtained at blockfrost.io.
For testing, we read the API key from the file BLOCKFROST_PROJECT_ID in the
root of our project (not shared in the git repository):
>>> api_key = ""
>>> import pathlib
>>> fname = str(pathlib.Path(__file__).parent.parent/'BLOCKFROST_PROJECT_ID')
>>> with open(fname) as f:
...     for line in f:
...         api_key = line.strip()

With a valid API key, we can initialise the API and query stake addresses for
existence:
>>> bf = BlockFrost(api_key)
>>> existing = "stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq"
>>> missing = "stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh"
>>> bf.check_stake_address(existing)
True
>>> bf.check_stake_address(missing)
False

With an invalid API key, the health query is still possible, but subsequent
queries fail:
>>> bf = BlockFrost("mainnetABCDEFGH")
>>> bf.check_stake_address(existing)
Traceback (most recent call last):
    ...
bfstakecheck.InactiveError: Invalid BlockFrost API key!
>>> bf.check_stake_address(missing)
Traceback (most recent call last):
    ...
bfstakecheck.InactiveError: Invalid BlockFrost API key!

The wrapper prevents subsequent calls to the API if one call has failed due
to invalid key, request limit, or server errors.
"""
from blockfrost import BlockFrostApi, ApiError  # type: ignore


class InactiveError(Exception):
    """Raised if the BlockFrost API is inactive for some reason."""

    pass


class BlockFrost:
    """Wrapper of BlockFrost to test stake keys."""

    def __init__(self, api_key: str) -> None:
        """Initialise BlockFrost API and test health."""
        self._blockfrost_api = BlockFrostApi(project_id=api_key)
        self._inactive = ""
        try:
            if not self._blockfrost_api.health().is_healthy:
                self._inactive = "BlockFrost API not healthy!"
        except ApiError as e:
            if e.status_code == 400:
                raise e
            elif e.status_code == 403:
                self._inactive = "Invalid BlockFrost API key!"
            elif e.status_code == 418 or e.status_code == 429:
                self._inactive = "Request limit for BlockFrost API reached!"
            elif e.status_code == 500:
                self._inactive = "BlockFrost API has internal server error!"
            if self._inactive:
                raise InactiveError(self._inactive)

    def check_stake_address(self, stake_address: str) -> bool:
        """Check if the stake address has been active on the blockchain."""
        if self._inactive:
            raise InactiveError(self._inactive)
        found = True
        try:
            self._blockfrost_api.account_addresses_total(stake_address)
        except ApiError as e:
            if e.status_code == 400:
                raise e
            elif e.status_code == 403:
                self._inactive = "Invalid BlockFrost API key!"
            elif e.status_code == 404:
                found = False
            elif e.status_code == 418 or e.status_code == 429:
                self._inactive = "Request limit for BlockFrost API reached!"
            elif e.status_code == 500:
                self._inactive = "BlockFrost API has internal server error!"
            if self._inactive:
                raise InactiveError(self._inactive)
        return found
