"""Tiny CLI so a coding agent (Claude Code, Cursor, Codex, any shell-using agent) can search the web
and read pages, paid per call with x402 (USDC on Base). No account, no API key.

pip install "x402[evm,requests]"
export PK=0x...your_wallet_key
python cwx.py search "your question"
python cwx.py read https://example.com
"""
import os
import sys

from eth_account import Account
from x402 import x402ClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client


def main(argv):
    if len(argv) < 2 or argv[0] not in ("search", "read"):
        sys.exit('usage: cwx.py search "query" | cwx.py read URL')
    client = x402ClientSync()
    register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["PK"])))
    http = x402_requests(client)
    if argv[0] == "search":
        r = http.get("https://search.cyberwarex.com/search",
                     params={"q": " ".join(argv[1:]), "max_results": 5}, timeout=60)
        r.raise_for_status()
        for h in r.json()["results"]:
            print(f"{h['title']}\n  {h['url']}\n  {h.get('snippet', '')}\n")
    else:
        r = http.get("https://web.cyberwarex.com/fetch", params={"url": argv[1], "format": "markdown"}, timeout=90)
        r.raise_for_status()
        print(r.json().get("content", "")[:20000])


if __name__ == "__main__":
    main(sys.argv[1:])
