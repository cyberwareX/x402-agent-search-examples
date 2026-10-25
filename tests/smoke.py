"""Free smoke test: every endpoint the examples call answers an unpaid request with an x402 v2 quote.
No wallet, no money. python tests/smoke.py"""
import base64
import json
import sys
import urllib.request

ENDPOINTS = [
    ("https://search.cyberwarex.com/search?q=test", 3000),
    ("https://search.cyberwarex.com/search-contents?q=test", 6000),
    ("https://web.cyberwarex.com/fetch?url=https://example.com", 1000),
]


def quote(url):
    req = urllib.request.Request(url, headers={"User-Agent": "x402-examples-smoke"})
    try:
        urllib.request.urlopen(req, timeout=20)
    except urllib.error.HTTPError as e:
        if e.code != 402:
            raise
        hdr = e.headers.get("PAYMENT-REQUIRED")
        body = json.loads(base64.b64decode(hdr)) if hdr else json.loads(e.read())
        return body["accepts"][0]
    raise AssertionError(f"{url} did not ask for payment")


failed = 0
for url, amount in ENDPOINTS:
    try:
        a = quote(url)
        assert a["network"] == "eip155:8453", a["network"]
        assert int(a["amount"]) == amount, (a["amount"], amount)
        print("ok  ", url, a["amount"])
    except Exception as e:  # report every endpoint, then fail
        failed += 1
        print("FAIL", url, repr(e))
sys.exit(1 if failed else 0)
