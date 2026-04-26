# poly_bot

A safe scaffold for monitoring and paper-trading BTC 5-minute direction ideas.

This repository is intentionally non-executing for live orders. It helps you:

- run on GitHub Actions every 5 minutes
- store sensitive values in GitHub Secrets
- mask sensitive values in logs
- compute a simple UP / DOWN / SKIP signal
- save local artifacts that show what the bot would do

## Sensitive values

Never commit these values to the repo:

- API keys
- API secrets or passphrases
- private keys or seed phrases
- webhook URLs with auth tokens
- account identifiers that become risky when combined with other secrets

## Files added for local use

```text
.env.example                 Local environment template
Makefile                     Local setup / test / run commands
src/bot/config.py            Environment loading
src/bot/redact.py            Secret masking helpers
src/bot/signal.py            Simple direction signal logic
src/bot/intent.py            Paper order intent generator
src/bot/state.py             State snapshot writer
src/bot/main.py              Main local entry point
tests/test_signal.py         Basic tests
```

## Local setup

Clone the repo, create a virtual environment, and install dependencies:

```bash
git clone https://github.com/yt-feng/poly_bot.git
cd poly_bot
make setup
```

Create your local env file:

```bash
cp .env.example .env
```

Edit `.env` and keep `DRY_RUN=true`. The placeholders in `.env.example` are there so you can see which fields are sensitive.

Run tests:

```bash
make test
```

Run the local paper bot:

```bash
make run
```

## What local run produces

A local run writes three files into `out/`:

- `decision.json` — redacted config plus signal result
- `order_intent.json` — what the bot would do in paper mode
- `state.json` — last run snapshot with timestamp

## Example signal behavior

Inputs:

- `ANCHOR_PRICE=100000`
- `CURRENT_PRICE=100050`
- `SIGNAL_THRESHOLD_BPS=5`

Output:

- move = +5 bps
- signal = `UP`
- order intent = `would_buy_up`

## GitHub Actions mode

The workflow runs every 5 minutes or can be triggered manually. It reads the same environment shape as local mode and uploads `out/decision.json` as an artifact.

## Public repo safety notes

A public repo can still use GitHub Secrets safely only if you:

- never print raw secrets
- do not commit `.env`
- keep workflow permissions minimal
- review third-party actions carefully

## Limit of this scaffold

This project stops at signal generation and paper order intent. It does not place live orders.

## License

MIT
