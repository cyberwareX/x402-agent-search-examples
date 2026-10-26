"""Exa-shaped web search with no API key: same request body as Exa's /search, paid per call with x402 ($0.005 USDC on Base).

pip install "x402[evm,requests]"
PK=0x...your_wallet_key python exa_shaped_search.py "your question"
Fields we do not support come back in ignoredFields. Results are a metasearch over public engines
(resolvedSearchType is always "keyword"), not Exa's neural index.
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

body = {"query": " ".join(sys.argv[1:]) or "x402 payment protocol", "numResults": 5,
        "contents": {"text": {"maxCharacters": 500}}}
r = http.post("https://search.cyberwarex.com/v1/search", json=body, timeout=60)
r.raise_for_status()
data = r.json()
for hit in data["results"]:
    print(hit["title"], "-", hit["url"])
    print("  ", (hit.get("text") or "")[:120].replace("\n", " "))
if data.get("ignoredFields"):
    print("ignored:", data["ignoredFields"])
