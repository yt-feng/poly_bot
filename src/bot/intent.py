from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .signal import SignalResult


ACTION_MAP = {
    "UP": "would_buy_up",
    "DOWN": "would_buy_down",
    "SKIP": "no_trade",
}


def build_order_intent(result: SignalResult) -> dict[str, Any]:
    return {
        "intent_type": "paper-order",
        "action": ACTION_MAP[result.signal],
        "market_type": "btc-5m-direction",
        "decision": asdict(result),
        "execution_enabled": False,
        "note": "This file describes what the bot would do, without placing a live order.",
    }
