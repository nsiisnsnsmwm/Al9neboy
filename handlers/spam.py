from pyrogram import Client, filters
from pyrogram.types import Message
from config import config

def setup(client: Client):
    @client.on_message(filters.command("spam") & filters.group)
    async def spam_message(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if len(message.command) < 3:
            await message.reply_text("Usage: /spam <count> <message>")
            return
            
        try:
            count = int(message.command[1])
            if count > 20:  # Limit to prevent abuse
                await message.reply_text("Maximum spam count is 20.")
                return
                
            spam_text = " ".join(message.command[2:])
            for _ in range(count):
                await message.reply_text(spam_text)
                await asyncio.sleep(1)  # Small delay to avoid flooding
                
        except ValueError:
            await message.reply_text("Please provide a valid number for count.")