"""CrewAI tool: web search for your crew, paid per call with x402 (USDC on Base). No API key.

pip install "x402[evm,requests]" crewai
PK=0x...your_wallet_key python search_tool.py
Then: Agent(role=..., goal=..., tools=[CyberwarexSearch()])
"""
import os

from crewai.tools import BaseTool
from eth_account import Account
from x402 import x402ClientSync
from x402.http.clients import x402_requests
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

_client = x402ClientSync()
register_exact_evm_client(_client, EthAccountSigner(Account.from_key(os.environ["PK"])))
_http = x402_requests(_client)


class CyberwarexSearch(BaseTool):
    name: str = "web_search"
    description: str = "Search the live web. Input: a search query. Output: up to 5 'title - url - snippet' lines."

    def _run(self, query: str) -> str:
        r = _http.get("https://search.cyberwarex.com/search", params={"q": query, "max_results": 5}, timeout=60)
        r.raise_for_status()
        return "\n".join(f"{h['title']} - {h['url']} - {h.get('snippet', '')}" for h in r.json()["results"])


if __name__ == "__main__":
    print(CyberwarexSearch().run("crewai web search tool"))
