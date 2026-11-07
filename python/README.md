# python

See the top-level README for price, speed and the free trial. Set PK to a wallet key with a little USDC on Base, then run the file.

`trade_gate.py base 0xTOKEN 100`: pays $0.005 for a token safety check, then prints BUY (full or a quarter size) or SKIP. It never trades and fails closed: no answer means no trade. Offline test: `python tests/test_trade_gate.py`.
