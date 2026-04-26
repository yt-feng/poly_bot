from __future__ import annotations

from typing import Dict, Mapping


def mask_secret(value: str | None, prefix: int = 3, suffix: int = 3) -> str:
    if not value:
        return "<empty>"
    if len(value) <= prefix + suffix:
        return "*" * len(value)
    return f"{value[:prefix]}...{value[-suffix:]}"


def redact_mapping(values: Mapping[str, str | None]) -> Dict[str, str]:
    return {key: mask_secret(value) for key, value in values.items()}


def emit_github_mask_commands(values: Mapping[str, str | None]) -> None:
    for value in values.values():
        if value:
            print(f"::add-mask::{value}")
