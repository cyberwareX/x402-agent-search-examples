# Claude Code: give it web search and page reading

1. Copy `cwx.py` and the `.claude/skills/web-search` folder into your project.
2. `pip install "x402[evm,requests]"` and `export PK=0x...` (a wallet with a little USDC on Base).
3. Ask Claude Code something that needs fresh facts. It finds the skill and runs `python cwx.py search ...`.

Cost: $0.003 per search, $0.001 per page read. Spend is capped by what you put in the wallet.
