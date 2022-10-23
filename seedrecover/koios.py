"""Test for active stake addresses through Koios.

>>> existing = "stake1u9t04dtwptk5776eluj6ruyd782k66npnf55tdrp6dvwnzs24r8yq"
>>> missing = "stake1u8p6x7049w05z8y2wqwfrdx04dzupzkye68qkv9zcec3dwqd9tweh"
>>> check_stake_address(existing)
True
>>> check_stake_address(missing)
False
"""
import json
from urllib.request import urlopen, Request

koios = "https://api.koios.rest/api/v0"
account_info_url = f"{koios}/account_info?select=stake_address"


def check_stake_address(stake_address: str) -> bool:
    """Check if the stake address has been active on the blockchain."""
    req_body = bytes(json.dumps({'_stake_addresses': [stake_address]}),
                     encoding='utf-8')
    req = Request(account_info_url, req_body)
    req.add_header('Content-Type', 'application/json')
    with urlopen(req) as account_info_response:
        account_info = json.loads(account_info_response.read().decode())
        if account_info:
            return True
        else:
            return False
