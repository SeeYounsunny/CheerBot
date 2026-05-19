"""JSON file storage for team members."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent


def data_dir() -> Path:
    """Directory for persistent data (override with DATA_DIR env)."""
    raw = os.getenv("DATA_DIR", "data").strip() or "data"
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path


def members_path() -> Path:
    return data_dir() / "members.json"


def ensure_members_file() -> None:
    path = members_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("{}", encoding="utf-8")


def load_members() -> dict[str, dict[str, Any]]:
    ensure_members_file()
    path = members_path()
    try:
        raw = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        logger.warning("Failed to read %s: %s", path, exc)
        return {}
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.warning("Invalid JSON in %s (%s); treating as empty", path, exc)
        return {}
    if not isinstance(data, dict):
        logger.warning("Expected JSON object in %s; treating as empty", path)
        return {}
    return data


def save_members(members: dict[str, dict[str, Any]]) -> None:
    path = members_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(members, ensure_ascii=False, indent=2)
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=".members-",
        suffix=".json.tmp",
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        tmp_path.replace(path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
