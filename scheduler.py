"""Daily morning cheer scheduler (KST)."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

from mbti_logic import pick_hero
from messages import morning_cheer_message
from storage import load_members

logger = logging.getLogger(__name__)

KST = ZoneInfo("Asia/Seoul")


def parse_cheer_time(value: str | None) -> tuple[int, int]:
    raw = (value or "09:00").strip()
    parts = raw.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid CHEER_TIME format: {raw!r} (expected HH:MM)")
    hour, minute = int(parts[0]), int(parts[1])
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Invalid CHEER_TIME: {raw!r}")
    return hour, minute


async def send_morning_cheer(bot: Bot, chat_id: str) -> None:
    members = load_members()
    if not members:
        logger.info("No members registered; skipping morning cheer.")
        return

    hero = pick_hero(members, when=datetime.now(KST))
    if hero is None:
        logger.info("No hero selected; skipping morning cheer.")
        return

    text = morning_cheer_message(hero)
    await bot.send_message(chat_id=chat_id, text=text)
    logger.info("Morning cheer sent for %s", hero.get("name"))


def setup_scheduler(bot: Bot, chat_id: str) -> AsyncIOScheduler:
    hour, minute = parse_cheer_time(os.getenv("CHEER_TIME"))
    scheduler = AsyncIOScheduler(timezone=KST)
    scheduler.add_job(
        send_morning_cheer,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="morning_cheer",
        replace_existing=True,
        kwargs={"bot": bot, "chat_id": chat_id},
    )
    scheduler.start()
    logger.info("Scheduled morning cheer at %02d:%02d KST", hour, minute)
    return scheduler
