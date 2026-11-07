"""Trade gate: before your agent buys a token, it pays $0.005 for a safety check and decides.

pip install "x402[evm,requests]"
PK=0x...your_wallet_key python trade_gate.py base 0xTOKEN [100]

The wallet needs a little USDC on Base (each check is $0.005, nothing else is charged).
The last argument is the size you planned to trade, in USD (default 100).
This script only decides. It never trades: plug the decision into your own buy code.
"""
import base64
import json
import os
import sys

from eth_account import Account
from x402 import x402ClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

CHECK_URL = "https://oracle.cyberwarex.com/risk/explain"

# What the agent does for each answer. LIMIT means "real risk found": trade a quarter, or skip.
SIZE_FACTOR = {"ALLOW": 1.0, "LIMIT": 0.25, "RECHECK": 0.0, "BLOCK": 0.0}


def check_token(http, chain, address):
    """Pay for one safety check and return the parsed answer, or None if it failed."""
    try:
        r = http.get(CHECK_URL, params={"chain": chain, "address": address}, timeout=60)
    except Exception as e:  # network error, or the wallet could not sign the payment
        print("check failed:", type(e).__name__, str(e)[:200])
        return None
    if r.status_code != 200:
        print("check failed: HTTP", r.status_code, r.text[:200])
        return None
    answer = r.json()
    receipt = r.headers.get("payment-response")
    if receipt:  # base64 JSON with the on-chain settlement transaction
        answer["_paid_tx"] = json.loads(base64.b64decode(receipt)).get("transaction")
    return answer


def decide(answer, planned_usd):
    """Turn the check into a trade size. No answer means no trade (fail closed)."""
    if not answer or answer.get("verdict") not in SIZE_FACTOR:
        return 0.0, "no usable safety answer, so no trade"
    verdict = answer["verdict"]
    size = round(planned_usd * SIZE_FACTOR[verdict], 2)
    why = answer.get("recommendation", {}).get("why") or verdict
    return size, why


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    chain, address = sys.argv[1], sys.argv[2]
    planned = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0

    client = x402ClientSync()
    register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["PK"])))
    http = x402_requests(client)

    answer = check_token(http, chain, address)
    size, why = decide(answer, planned)
    if answer:
        codes = answer.get("recommendation", {}).get("reason_codes", [])
        print(f"{answer['verdict']} grade {answer.get('grade')} risk {answer.get('risk', {}).get('overall')}/100")
        print("codes:", ", ".join(codes) or "none")
        if answer.get("_paid_tx"):
            print("paid $0.005, tx https://basescan.org/tx/" + answer["_paid_tx"])
    print("why:", why)
    if size > 0:
        print(f"decision: BUY ${size} (planned ${planned})")
    else:
        print("decision: SKIP")


if __name__ == "__main__":
    main()
