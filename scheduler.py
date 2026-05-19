"""Daily morning cheer scheduler (KST) for Railway polling."""

from __future__ import annotations

import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

from cheer import run_morning_cheer

logger = logging.getLogger(__name__)


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
    del bot, chat_id
    ok, message = run_morning_cheer()
    logger.info(message if ok else "Morning cheer failed: %s", message)


def setup_scheduler(bot: Bot, chat_id: str) -> AsyncIOScheduler:
    from zoneinfo import ZoneInfo

    hour, minute = parse_cheer_time(os.getenv("CHEER_TIME"))
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Seoul"))
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
