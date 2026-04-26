from __future__ import annotations

import os
from dataclasses import asdict, dataclass

from .redact import redact_mapping


@dataclass
class Config:
    anchor_price: float
    current_price: float
    signal_threshold_bps: float
    dry_run: bool
    polymarket_api_key: str | None
    polymarket_secret: str | None
    polymarket_passphrase: str | None
    polymarket_proxy_wallet: str | None
    polymarket_funder: str | None
    alert_webhook_url: str | None

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            anchor_price=float(os.getenv("ANCHOR_PRICE", "0")),
            current_price=float(os.getenv("CURRENT_PRICE", "0")),
            signal_threshold_bps=float(os.getenv("SIGNAL_THRESHOLD_BPS", "5")),
            dry_run=os.getenv("DRY_RUN", "true").lower() == "true",
            polymarket_api_key=os.getenv("POLYMARKET_API_KEY"),
            polymarket_secret=os.getenv("POLYMARKET_SECRET"),
            polymarket_passphrase=os.getenv("POLYMARKET_PASSPHRASE"),
            polymarket_proxy_wallet=os.getenv("POLYMARKET_PROXY_WALLET"),
            polymarket_funder=os.getenv("POLYMARKET_FUNDER"),
            alert_webhook_url=os.getenv("ALERT_WEBHOOK_URL"),
        )

    def redacted_snapshot(self) -> dict[str, object]:
        raw = asdict(self)
        secrets = {
            "polymarket_api_key": self.polymarket_api_key,
            "polymarket_secret": self.polymarket_secret,
            "polymarket_passphrase": self.polymarket_passphrase,
            "polymarket_proxy_wallet": self.polymarket_proxy_wallet,
            "polymarket_funder": self.polymarket_funder,
            "alert_webhook_url": self.alert_webhook_url,
        }
        raw.update(redact_mapping(secrets))
        return raw
