from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_state(data: dict[str, Any], out_dir: Path) -> Path:
    state = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    path = out_dir / "state.json"
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return path
