# x402 agent search examples

**CyberWareX: web search, web page reading and token safety checks for AI agents, paid per call in USDC with x402. No account, no API key.**

Copy-paste examples that give an AI agent live web search and page reading. The agent pays for each
call from its own wallet with [x402](https://x402.org) (USDC on Base). There is no signup, no key to
leak, and no monthly plan. The payment is gasless for the payer: the wallet only needs USDC.

| Folder | What it is |
|---|---|
| [python](python) | `search.py` and `read_page.py`, plain `requests` |
| [typescript](typescript) | `search.mjs` with `@x402/fetch` |
| [langchain](langchain) | `web_search` and `read_page` tools for LangChain or LangGraph |
| [crewai](crewai) | `CyberwarexSearch` tool for a crew |
| [claude-code](claude-code) | a skill plus a tiny CLI (`cwx.py`) Claude Code runs |
| [cursor](cursor) | a Cursor rule that uses the same CLI |

Every example here was run against the live service with a real paid call on 2026-10-25.

## Try it with no wallet first

```bash
curl -H 'X-Free-Trial: 1' 'https://search.cyberwarex.com/search?q=x402+payment+protocol'
```

3 free searches per day per IP. A real paid answer with its on-chain receipt: `https://search.cyberwarex.com/sample`.

## Python in 10 lines

```python
# pip install "x402[evm,requests]"   then: PK=0x... python search.py
import os
from eth_account import Account
from x402 import x402ClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

client = x402ClientSync()
register_exact_evm_client(client, EthAccountSigner(Account.from_key(os.environ["PK"])))
r = x402_requests(client).get("https://search.cyberwarex.com/search", params={"q": "x402", "max_results": 5})
print(r.json()["results"])
```

## Price and speed (real numbers)

| Call | Price | Median time | 90% of calls under |
|---|---|---|---|
| `GET search.cyberwarex.com/search` | $0.003 | 2.0 s | 3.1 s |
| `GET search.cyberwarex.com/search-contents` (results plus page text) | $0.006 | 7.3 s | 10.2 s |
| `GET web.cyberwarex.com/fetch` (page as markdown, JavaScript rendered) | $0.001 | 5.0 s | 16.6 s |

Times are from our own server logs of successful calls (1,146 searches, 1,191 search-contents, 8,295 page reads),
counted on 2026-10-25. An Exa-shaped `POST /v1/search` ($0.005) and `/v1/contents` also exist for code already written for Exa.

## Use something else when

- You need very high volume at a flat monthly price: a keyed plan from a large search API is cheaper at scale.
- You want neural or semantic search over a curated index: our search is a metasearch over public engines (SearXNG),
  so result quality follows those engines.
- Your agent cannot hold a crypto wallet, or your company cannot pay in USDC.
- You need a written uptime guarantee: we are a small operator and offer none.

## Machine-readable

- Catalog for agents: https://cyberwarex.com/llms.txt and https://cyberwarex.com/.well-known/x402
- Plain answers to common questions: https://cyberwarex.com/answers (for example https://cyberwarex.com/answers/x402-search-api-example)
- Contact: x402@cyberwarex.com

MIT license.
