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


def run_morning_cheer() -> tuple[bool, str]:
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        return False, "TELEGRAM_CHAT_ID is not set"

    now = datetime.now(KST)
    if now.weekday() >= 5:
        return True, "Weekend; skipped."

    members = load_members()
    if not members:
        return True, "No members registered; skipped."

    hero = pick_hero(members, when=now)
    if hero is None:
        return True, "No hero selected; skipped."

    text = morning_cheer_message(hero)
    send_message(chat_id, text)
    message = f"Morning cheer sent for {hero.get('name')}"
    logger.info(message)
    return True, message
