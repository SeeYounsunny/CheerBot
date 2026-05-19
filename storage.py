"""JSON file storage for team members."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MEMBERS_PATH = Path(__file__).resolve().parent / "data" / "members.json"


def ensure_members_file() -> None:
    MEMBERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not MEMBERS_PATH.exists():
        MEMBERS_PATH.write_text("{}", encoding="utf-8")


def load_members() -> dict[str, dict[str, Any]]:
    ensure_members_file()
    raw = MEMBERS_PATH.read_text(encoding="utf-8").strip()
    if not raw:
        return {}
    return json.loads(raw)


def save_members(members: dict[str, dict[str, Any]]) -> None:
    ensure_members_file()
    MEMBERS_PATH.write_text(
        json.dumps(members, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
