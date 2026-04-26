from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .config import Config
from .intent import build_order_intent
from .redact import emit_github_mask_commands
from .signal import compute_signal
from .state import write_state


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

    decision_path = out_dir / "decision.json"
    decision_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    intent = build_order_intent(result)
    intent_path = out_dir / "order_intent.json"
    intent_path.write_text(json.dumps(intent, indent=2), encoding="utf-8")

    state_path = write_state(
        {
            "mode": payload["mode"],
            "signal": result.signal,
            "anchor_price": result.anchor_price,
            "current_price": result.current_price,
            "threshold_bps": result.threshold_bps,
            "move_bps": result.move_bps,
        },
        out_dir,
    )

    print(json.dumps(payload, indent=2))
    print(json.dumps(intent, indent=2))
    print(f"Saved decision artifact to {decision_path}")
    print(f"Saved order intent to {intent_path}")
    print(f"Saved state snapshot to {state_path}")


if __name__ == "__main__":
    main()
