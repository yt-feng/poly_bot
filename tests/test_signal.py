from bot.signal import compute_move_bps, compute_signal


def test_compute_move_bps_positive() -> None:
    assert round(compute_move_bps(100.0, 101.0), 2) == 100.0


def test_compute_signal_up() -> None:
    result = compute_signal(100.0, 100.1, 5.0)
    assert result.signal == "UP"


def test_compute_signal_down() -> None:
    result = compute_signal(100.0, 99.9, 5.0)
    assert result.signal == "DOWN"


def test_compute_signal_skip() -> None:
    result = compute_signal(100.0, 100.01, 5.0)
    assert result.signal == "SKIP"
