"""Web search for an AI agent, paid per call with x402 (USDC on Base). No account, no API key.

pip install "x402[evm,requests]"
PK=0x...your_wallet_key python search.py "your question"
The wallet needs a little USDC on Base. No ETH needed: the payment is gasless for you.
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

query = " ".join(sys.argv[1:]) or "x402 payment protocol"
r = http.get("https://search.cyberwarex.com/search", params={"q": query, "max_results": 5}, timeout=60)
r.raise_for_status()
for hit in r.json()["results"]:
    print(hit["title"], "-", hit["url"])
