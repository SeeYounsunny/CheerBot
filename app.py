"""MBTI morning cheer Telegram bot (Railway polling + APScheduler)."""

from __future__ import annotations

import logging
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from handlers import handle_mbti_command, handle_test_command
from scheduler import setup_scheduler

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class _HealthHandler(BaseHTTPRequestHandler):
    """Minimal handler so Railway web health checks see an open PORT."""

    def log_message(self, format: str, *args: object) -> None:
        del format, args

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok\n")


def _start_health_server() -> None:
    port_raw = os.getenv("PORT")
    if not port_raw:
        logger.info("PORT not set; health HTTP server skipped (worker mode)")
        return
    try:
        port = int(port_raw)
    except ValueError:
        logger.error("Invalid PORT=%r; cannot start health server", port_raw)
        return
    server = HTTPServer(("0.0.0.0", port), _HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info("Health check HTTP server listening on 0.0.0.0:%s", port)


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value
    logger.error("Missing required environment variable: %s", name)
    logger.error(
        "Set it in Railway → Service → Variables (or .env for local dev)."
    )
    sys.exit(1)


_CHAT_TYPE_LABELS = {
    "private": "개인",
    "group": "그룹",
    "supergroup": "슈퍼그룹",
    "channel": "채널",
}


async def chatid_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.effective_chat is None:
        return

    chat = update.effective_chat
    chat_id = chat.id
    chat_type = chat.type
    type_label = _CHAT_TYPE_LABELS.get(chat_type, chat_type)
    reply = f"이 채팅방 ID: `{chat_id}`\n채팅 유형: {type_label}"
    await update.message.reply_text(reply, parse_mode="Markdown")
    logger.info("Handled /chatid: chat_id=%s type=%s", chat_id, chat_type)


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


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    reply = handle_test_command()
    await update.message.reply_text(reply)
    logger.info("Handled /test preview")


def main() -> None:
    load_dotenv()
    logger.info("CheerBot starting (Python %s)", sys.version.split()[0])

    token = _require_env("TELEGRAM_BOT_TOKEN")
    chat_id = _require_env("TELEGRAM_CHAT_ID")
    cheer_time = os.getenv("CHEER_TIME", "09:00").strip() or "09:00"
    logger.info(
        "Config: TELEGRAM_CHAT_ID=%s CHEER_TIME=%s",
        chat_id,
        cheer_time,
    )

    _start_health_server()

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
    application.add_handler(CommandHandler("chatid", chatid_command))
    application.add_handler(CommandHandler("mbti", mbti_command))
    application.add_handler(CommandHandler("test", test_command))

    logger.info("Starting MBTI cheer bot (polling mode)...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
