// Web search for an AI agent, paid per call with x402 (USDC on Base). No account, no API key.
// npm i @x402/fetch @x402/evm viem
// PK=0x...your_wallet_key node search.mjs "your question"
import { wrapFetchWithPaymentFromConfig } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm";
import { privateKeyToAccount } from "viem/accounts";

const pay = wrapFetchWithPaymentFromConfig(fetch, {
  schemes: [{ network: "eip155:8453", client: new ExactEvmScheme(privateKeyToAccount(process.env.PK)) }], // Base mainnet
});

const query = process.argv.slice(2).join(" ") || "x402 payment protocol";
const r = await pay(`https://search.cyberwarex.com/search?q=${encodeURIComponent(query)}&max_results=5`);
if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
const { results } = await r.json();
for (const hit of results) console.log(hit.title, "-", hit.url);
