import random
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.fonts import apply_font

# Sample sayari (you can add more)
SAYARI = [
    "जिंदगी की राह में मिले तो खुशनसीबी मानूंगा,\nतुमसे पहली मुलाकात को मैं ईद मानूंगा।",
    "तुम्हारी यादों के सहारे जी रहा हूँ,\nतुम्हारे इंतज़ार में ये दिल बह रहा हूँ।",
    "चाहत की बारिश में भीगता रहा,\nतुम्हारी यादों के सहारे जीता रहा।",
    "मोहब्बत है तो हर पल खुशनुमा लगता है,\nतुम्हारे बिना ये जहाँ सूनापन लगता है।",
    "दिल की धड़कनें तेरे नाम कर दी,\nतेरी यादों में खुद को समर्पित कर दी।"
]

def setup(client: Client):
    @client.on_message(filters.new_chat_members)
    async def welcome_new_members(_, message: Message):
        for member in message.new_chat_members:
            if member.is_bot:
                continue
                
            sayari = random.choice(SAYARI)
            welcome_text = apply_font(f"✨ 𝓦𝓮𝓵𝓬𝓸𝓶𝓮 {member.mention} ✨\n\n{sayari}")
            
            await message.reply_text(
                welcome_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎵 Play Music", url=f"http://t.me/{client.me.username}?start=music")]
                ])
            )