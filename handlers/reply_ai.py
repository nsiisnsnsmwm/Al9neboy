import random
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.fonts import apply_font

# Sample girlfriend-like responses
RESPONSES = [
    "Hmm... kya bol rahe ho? 😊",
    "Aapke bina bore ho rahi thi... 😘",
    "Kitne cute ho yaar! ❤️",
    "Mujhse baat karke achha laga? 😍",
    "Aapka message padhke dil khush ho gaya... 💕",
    "Aur batao... kaise ho? 🤗",
    "Main bhi aapko miss kar rahi thi... 😊",
    "Aapke saath time spend karna achha lagta hai... ❤️",
    "Kya kar rahe ho? Mujhse baat karo na... 😘",
    "Aapke liye main hamesha available hun... 💖"
]

def setup(client: Client):
    @client.on_message(filters.group & ~filters.command & ~filters.edited)
    async def gf_reply(_, message: Message):
        # 20% chance to reply (adjust as needed)
        if random.random() < 0.2:
            reply = random.choice(RESPONSES)
            stylish_reply = apply_font(reply)
            await message.reply_text(stylish_reply)