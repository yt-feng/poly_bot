# poly_bot

A **safe, public-repo friendly scaffold** for monitoring and paper-trading BTC 5-minute direction ideas.

This repository is intentionally **non-executing** for live orders. It is designed to help you:

- run on GitHub Actions every 5 minutes
- store sensitive values in GitHub Secrets
- mask sensitive values in logs
- compute a simple UP / DOWN / SKIP signal
- save a decision artifact for review

## What is considered sensitive

These values should **never** be committed to the repo:

- API keys
- API secrets / passphrases
- private keys / seed phrases / wallet signing material
- webhook URLs with auth tokens
- account identifiers that could be abused together with other secrets

This repo demonstrates how to **dummy** or **mask** them.

## Dummy secret names

Configure these in **GitHub Settings -> Secrets and variables -> Actions**.

- `POLYMARKET_API_KEY`
- `POLYMARKET_SECRET`
- `POLYMARKET_PASSPHRASE`
- `POLYMARKET_PROXY_WALLET`
- `POLYMARKET_FUNDER`
- `ALERT_WEBHOOK_URL`

You can initially put dummy values such as:

```text
POLYMARKET_API_KEY=dummy_api_key_123456
POLYMARKET_SECRET=dummy_secret_abcdef
POLYMARKET_PASSPHRASE=dummy_passphrase
POLYMARKET_PROXY_WALLET=0x0000000000000000000000000000000000000000
POLYMARKET_FUNDER=0x0000000000000000000000000000000000000000
ALERT_WEBHOOK_URL=https://example.com/webhook/dummy
```

## What gets masked

The code registers GitHub Actions mask commands for the sensitive values it sees, and also produces a redacted config snapshot.

Example:

```text
POLYMARKET_API_KEY -> dum...456
POLYMARKET_SECRET -> dum...def
ALERT_WEBHOOK_URL -> htt...mmy
```

## Repository layout

```text
.github/workflows/paper-bot.yml   Scheduled workflow
src/bot/config.py                 Environment loading
src/bot/redact.py                 Secret masking helpers
src/bot/signal.py                 Simple direction signal logic
src/bot/main.py                   Entry point for dry-run decisions
tests/test_signal.py              Basic tests
```

## How it works

The workflow runs every 5 minutes or can be triggered manually.

The script:

1. loads env vars and GitHub Secrets
2. masks sensitive values for logs
3. reads `ANCHOR_PRICE` and `CURRENT_PRICE`
4. computes a signal: `UP`, `DOWN`, or `SKIP`
5. writes a JSON artifact to `out/decision.json`

No live order placement is implemented in this repo.

## Manual workflow inputs

The workflow supports manual inputs:

- `anchor_price`
- `current_price`
- `threshold_bps`

This makes it easy to test without any external API.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANCHOR_PRICE=100000
export CURRENT_PRICE=100150
export SIGNAL_THRESHOLD_BPS=5
PYTHONPATH=src python -m bot.main
```

## Public repo safety notes

A public repo can still use GitHub Secrets safely **only if** you keep these habits:

- never print raw secrets
- do not commit `.env`
- keep workflow permissions minimal
- review third-party actions carefully
- prefer pinning actions to a commit SHA later if you keep real secrets

## Next safe extension ideas

- add market data fetchers without execution
- add Slack / webhook alerts
- add state tracking between runs
- add paper PnL tracking

## License

MIT
