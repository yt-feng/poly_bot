from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignalResult:
    anchor_price: float
    current_price: float
    move_bps: float
    threshold_bps: float
    signal: str


def compute_move_bps(anchor_price: float, current_price: float) -> float:
    if anchor_price <= 0:
        raise ValueError("anchor_price must be greater than zero")
    return ((current_price - anchor_price) / anchor_price) * 10000.0


def compute_signal(anchor_price: float, current_price: float, threshold_bps: float) -> SignalResult:
    move_bps = compute_move_bps(anchor_price, current_price)
    if move_bps >= threshold_bps:
        signal = "UP"
    elif move_bps <= -threshold_bps:
        signal = "DOWN"
    else:
        signal = "SKIP"

    return SignalResult(
        anchor_price=anchor_price,
        current_price=current_price,
        move_bps=move_bps,
        threshold_bps=threshold_bps,
        signal=signal,
    )
