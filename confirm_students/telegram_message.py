from aiogram import Bot
from aiogram.enums import ParseMode
from django.conf import settings

async def send_telegram_message(telegram_id, message):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(telegram_id, message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Error sending message: {e}")