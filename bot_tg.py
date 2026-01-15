from aiogram import Bot

BOT_TOKEN = "8577276523:AAFLwxiHUPuBmmUOgolyQ49AMbQvS2aYezk"
CHAT_ID = 7034143307

bot = Bot(token=BOT_TOKEN)

async def send_telegram_message(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message)
