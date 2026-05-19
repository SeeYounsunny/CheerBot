"""MBTI morning cheer Telegram bot (Railway polling + APScheduler)."""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from handlers import handle_mbti_command
from scheduler import setup_scheduler

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def mbti_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.effective_user is None:
        return

    user = update.effective_user
    mbti_raw = " ".join(context.args) if context.args else ""
    reply = handle_mbti_command(
        str(user.id),
        user.first_name or user.username or "팀원",
        user.username,
        mbti_raw,
    )
    await update.message.reply_text(reply)
    logger.info("Handled /mbti for user %s", user.id)


def main() -> None:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    cheer_time = os.getenv("CHEER_TIME", "09:00")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN environment variable is required")
    if not chat_id:
        raise SystemExit("TELEGRAM_CHAT_ID environment variable is required")

    async def post_init(app: Application) -> None:
        # Clear any Vercel/webhook setup so polling does not conflict (HTTP 409).
        await app.bot.delete_webhook(drop_pending_updates=True)
        logger.info(
            "Webhook cleared; polling mode active (CHEER_TIME=%s KST)",
            cheer_time,
        )
        setup_scheduler(app.bot, chat_id)

    application = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )
    application.add_handler(CommandHandler("mbti", mbti_command))

    logger.info("Starting MBTI cheer bot (polling mode)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
