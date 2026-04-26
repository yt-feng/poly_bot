from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .config import Config
from .redact import emit_github_mask_commands
from .signal import compute_signal


def main() -> None:
    config = Config.from_env()

    sensitive_values = {
        "POLYMARKET_API_KEY": config.polymarket_api_key,
        "POLYMARKET_SECRET": config.polymarket_secret,
        "POLYMARKET_PASSPHRASE": config.polymarket_passphrase,
        "POLYMARKET_PROXY_WALLET": config.polymarket_proxy_wallet,
        "POLYMARKET_FUNDER": config.polymarket_funder,
        "ALERT_WEBHOOK_URL": config.alert_webhook_url,
    }
    emit_github_mask_commands(sensitive_values)

    result = compute_signal(
        anchor_price=config.anchor_price,
        current_price=config.current_price,
        threshold_bps=config.signal_threshold_bps,
    )

    payload = {
        "mode": "dry-run" if config.dry_run else "unsafe-disabled",
        "config": config.redacted_snapshot(),
        "decision": asdict(result),
        "note": "This scaffold computes a paper signal and does not place live orders.",
    }

    out_dir = Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "decision.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"Saved decision artifact to {out_path}")


if __name__ == "__main__":
    main()
