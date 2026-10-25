"""Let an agent read any web page as clean markdown (JavaScript rendered), paid per call with x402.

pip install "x402[evm,requests]"
PK=0x...your_wallet_key python read_page.py https://example.com
"""
import os
import sys

from eth_account import Account
from x402 import x402ClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

client = x402ClientSync()
register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["PK"])))
http = x402_requests(client)

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
r = http.get("https://web.cyberwarex.com/fetch", params={"url": url, "format": "markdown"}, timeout=90)
r.raise_for_status()
print(r.json().get("content", r.text)[:2000])
