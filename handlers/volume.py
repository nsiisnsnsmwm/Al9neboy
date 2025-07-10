from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import config
from utils.vc_handler import vc_handler

def setup(client: Client, user: Client):
    @client.on_message(filters.command("volume") & filters.group)
    async def set_volume(_, message: Message):
        chat_id = message.chat.id
        
        if chat_id not in vc_handler.vc_status or not vc_handler.vc_status[chat_id].is_connected:
            await message.reply_text("Not connected to voice chat.")
            return
            
        if len(message.command) < 2:
            current_vol = vc_handler.vc_status[chat_id].volume
            await message.reply_text(f"Current volume: {current_vol}%")
            return
            
        try:
            volume = int(message.command[1])
            if volume < 0 or volume > 200:
                await message.reply_text("Volume must be between 0 and 200.")
                return
                
            await vc_handler.vc_status[chat_id].set_volume(volume)
            await message.reply_text(f"Volume set to {volume}%")
        except ValueError:
            await message.reply_text("Please provide a valid number for volume.")

    @client.on_callback_query(filters.regex(r"^vol_(up|down)$"))
    async def volume_callback(_, query: CallbackQuery):
        chat_id = query.message.chat.id
        
        if chat_id not in vc_handler.vc_status or not vc_handler.vc_status[chat_id].is_connected:
            await query.answer("Not connected to voice chat.")
            return
            
        vc = vc_handler.vc_status[chat_id]
        direction = query.data.split("_")[1]
        
        if direction == "up":
            new_vol = min(200, vc.volume + 10)
        else:
            new_vol = max(0, vc.volume - 10)
            
        await vc.set_volume(new_vol)
        await query.answer(f"Volume set to {new_vol}%")
        
        # Update the volume display
        await query.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔈", callback_data="vol_down"),
                    InlineKeyboardButton("🔊", callback_data="vol_up")
                ]
            ])
        )