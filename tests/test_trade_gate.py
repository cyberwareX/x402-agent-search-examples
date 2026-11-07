"""Offline test of the trade gate decision rule (no wallet, no network). python tests/test_trade_gate.py"""
import importlib.util
import pathlib
import sys
import types

# trade_gate imports the x402 client at module load; stub it so this test needs no packages.
for name in ["eth_account", "x402", "x402.http", "x402.http.clients", "x402.mechanisms",
             "x402.mechanisms.evm", "x402.mechanisms.evm.exact", "x402.mechanisms.evm.exact.register"]:
    mod = sys.modules.setdefault(name, types.ModuleType(name))
    for attr in ["Account", "x402ClientSync", "x402_requests", "EthAccountSigner", "register_exact_evm_client"]:
        setattr(mod, attr, None)

path = pathlib.Path(__file__).resolve().parent.parent / "python" / "trade_gate.py"
spec = importlib.util.spec_from_file_location("trade_gate", path)
tg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tg)

cases = [
    (None, 0.0),                                       # check failed -> no trade
    ({}, 0.0),                                         # no verdict -> no trade
    ({"verdict": "MAYBE"}, 0.0),                       # unknown word -> no trade
    ({"verdict": "BLOCK", "recommendation": {"why": "honeypot"}}, 0.0),
    ({"verdict": "RECHECK"}, 0.0),
    ({"verdict": "LIMIT"}, 25.0),
    ({"verdict": "ALLOW"}, 100.0),
]
failed = 0
for answer, want in cases:
    size, why = tg.decide(answer, 100.0)
    ok = size == want and why
    failed += not ok
    print("ok  " if ok else "FAIL", answer, "->", size, why)
sys.exit(1 if failed else 0)
