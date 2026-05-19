"""Shared command handlers for Telegram /mbti."""

from __future__ import annotations

from datetime import datetime

from mbti_logic import is_valid_mbti
from messages import registration_confirm
from storage import load_members, save_members


def handle_mbti_command(
    user_id: str,
    display_name: str,
    username: str | None,
    mbti_raw: str,
) -> str:
    if not mbti_raw.strip():
        return "사용법: /mbti INFP (16가지 MBTI 중 하나)"

    mbti = mbti_raw.strip().upper()
    if not is_valid_mbti(mbti):
        return "올바른 MBTI 타입이 아니에요. 예: INFP, ENTJ (16가지)"

    members = load_members()
    members[user_id] = {
        "name": display_name,
        "username": username,
        "mbti": mbti,
        "registered_at": datetime.now().isoformat(timespec="seconds"),
    }
    save_members(members)
    return registration_confirm(display_name, mbti)
