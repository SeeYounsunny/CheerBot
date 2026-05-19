"""MBTI morning cheer Telegram bot."""

from __future__ import annotations

import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from mbti_logic import is_valid_mbti
from messages import registration_confirm
from scheduler import setup_scheduler
from storage import load_members, save_members

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def mbti_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.effective_user is None:
        return

    if not context.args:
        await update.message.reply_text("사용법: /mbti INFP (16가지 MBTI 중 하나)")
        return

    mbti = context.args[0].upper()
    if not is_valid_mbti(mbti):
        await update.message.reply_text(
            "올바른 MBTI 타입이 아니에요. 예: INFP, ENTJ (16가지)"
        )
        return

    user = update.effective_user
    display_name = user.first_name or user.username or "팀원"
    user_id = str(user.id)

    members = load_members()
    members[user_id] = {
        "name": display_name,
        "username": user.username,
        "mbti": mbti,
        "registered_at": datetime.now().isoformat(timespec="seconds"),
    }
    save_members(members)

    await update.message.reply_text(registration_confirm(display_name, mbti))
    logger.info("Registered %s (%s) as %s", display_name, user_id, mbti)


def main() -> None:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required in .env")
    if not chat_id:
        raise SystemExit("TELEGRAM_CHAT_ID is required in .env")

    async def post_init(app: Application) -> None:
        setup_scheduler(app.bot, chat_id)

    application = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )
    application.add_handler(CommandHandler("mbti", mbti_command))

    logger.info("Starting MBTI cheer bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
