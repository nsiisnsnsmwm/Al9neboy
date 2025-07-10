import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import config
from handlers import (
    music, admin, spam, welcome, volume, reply_ai
)
from utils.vc_handler import VoiceChat, vc_status
from utils import yt_search
from utils.vc_handler import VoiceChat, vc_status
from utils.vc_handler import VoiceChat, vc_status

app = Client(
    "vishal_music_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

user = Client(
    config.SESSION_STRING,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# Initialize handlers
music.setup(app, user)
admin.setup(app)
spam.setup(app)
welcome.setup(app)
volume.setup(app, user)
reply_ai.setup(app)

# Start command
@app.on_message(filters.command("start"))
async def start(_, message: Message):
    stylish_text = "✨ 𝓦�𝓮𝓵𝓬𝓸𝓶𝓮 𝓽𝓸 𝓥𝓲𝓼𝓱𝓪� 𝓜𝓾𝓼𝓲𝓬 𝓑𝓸𝓽 ✨"
    await message.reply_text(
        stylish_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📌 Add Me To Your Group", url=f"http://t.me/{app.me.username}?startgroup=true")],
            [InlineKeyboardButton("📣 Updates Channel", url="https://t.me/vishal_updates")]
        ])
    )

async def main():
    await app.start()
    await user.start()
    print("Bot started successfully!")
    await idle()
    await app.stop()
    await user.stop()

if __name__ == "__main__":
    asyncio.run(main())