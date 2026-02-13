# Bankr Trading Setup

## Status: Awaiting API Key + Funding

## Installation
- CLI: `npm install -g @bankr/cli` ✅ COMPLETED
- Location: `/home/solumieai/.npm-global/bin/bankr`

## Configuration Needed
1. **API Key** from https://bankr.bot/api
2. **Login command:** `bankr login --api-key bk_YOUR_KEY`
3. **Verification:** `bankr whoami`

## Wallets (Auto-Created on Signup)
- **EVM:** Base, Ethereum, Polygon, Unichain (auto-generated)
- **Solana:** Auto-generated
- **Funding:** User will send crypto to Solana address on next paycheck

## Trading Strategy (Experimental)
- **Start small:** $5-10 test trades
- **Chain preference:** Base (lowest gas fees)
- **Initial approach:** 
  1. Check balances
  2. Market research (trending tokens)
  3. Small test swaps
  4. Document all trades in memory/

## Safety Measures
- Using dedicated agent wallet (isolated from user funds)
- Read-only API key option available for monitoring
- IP whitelisting possible
- Rate limits: 100 msgs/day (can upgrade to Bankr Club for 1,000/day)

## Capabilities Enabled
- ✅ Token swaps (Base, Solana, etc.)
- ✅ Portfolio tracking
- ✅ Market research
- ✅ Limit orders / Stop loss
- ✅ DCA strategies
- ✅ NFT operations
- ✅ Polymarket betting
- ✅ Leverage trading (up to 50x)
- ✅ Token deployment (Clanker on Base, LaunchLab on Solana)

## Documentation
- Full skill docs: `/bankrbot-skills/bankr/`
- References: API workflow, trading, safety, error handling
- LLM Gateway: Could replace OpenRouter for some calls

## Next Steps (When User Ready)
1. User generates API key at bankr.bot/api
2. User sends Solana funding
3. Dexie logs in with API key
4. Start with balance check + small test trade
5. Document all activity in memory/

## Notes
- This is experimental trading with test funds
- Goal: See what free/low-cost automation is possible
- Loss acceptable as learning expense
- All trades logged for transparency

Ready for activation when API key + funds provided.