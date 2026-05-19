"""Morning cheer job for APScheduler on Railway."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from mbti_logic import pick_hero
from messages import morning_cheer_message
from storage import load_members
from telegram_client import send_message

logger = logging.getLogger(__name__)

KST = ZoneInfo("Asia/Seoul")

NO_MEMBERS_MESSAGE = (
    "아직 등록된 팀원이 없어요. /mbti 로 MBTI를 등록해 주세요!"
)
PREVIEW_PREFIX = "🧪 테스트 미리보기"


def build_morning_cheer_message(
    *,
    when: datetime | None = None,
    skip_weekend: bool = True,
    preview_prefix: str | None = None,
    empty_members_message: str | None = None,
) -> str | None:
    """Build morning cheer text. None means nothing to send (scheduled skip)."""
    members = load_members()
    if not members:
        return empty_members_message

    now = when or datetime.now(KST)
    if skip_weekend and now.weekday() >= 5:
        return None

    hero = pick_hero(members, when=now)
    if hero is None:
        return None

    text = morning_cheer_message(hero)
    if preview_prefix:
        return f"{preview_prefix}\n\n{text}"
    return text


def run_morning_cheer() -> tuple[bool, str]:
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        return False, "TELEGRAM_CHAT_ID is not set"

    now = datetime.now(KST)
    if now.weekday() >= 5:
        return True, "Weekend; skipped."

    text = build_morning_cheer_message(when=now)
    if text is None:
        return True, "No members registered; skipped."

    send_message(chat_id, text)
    message = f"Morning cheer sent"
    logger.info(message)
    return True, message
