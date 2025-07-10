from pyrogram import Client, filters
from pyrogram.types import Message
from config import config

def setup(client: Client):
    @client.on_message(filters.command("ban") & filters.group)
    async def ban_user(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if not message.reply_to_message:
            await message.reply_text("Reply to a user's message to ban them.")
            return
            
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        
        try:
            await client.ban_chat_member(chat_id, user_id)
            await message.reply_text(f"User {message.reply_to_message.from_user.mention} has been banned.")
        except Exception as e:
            await message.reply_text(f"Failed to ban user: {e}")

    @client.on_message(filters.command("unban") & filters.group)
    async def unban_user(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if not message.reply_to_message:
            await message.reply_text("Reply to a user's message to unban them.")
            return
            
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        
        try:
            await client.unban_chat_member(chat_id, user_id)
            await message.reply_text(f"User {message.reply_to_message.from_user.mention} has been unbanned.")
        except Exception as e:
            await message.reply_text(f"Failed to unban user: {e}")

    @client.on_message(filters.command("kick") & filters.group)
    async def kick_user(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if not message.reply_to_message:
            await message.reply_text("Reply to a user's message to kick them.")
            return
            
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        
        try:
            await client.ban_chat_member(chat_id, user_id)
            await client.unban_chat_member(chat_id, user_id)
            await message.reply_text(f"User {message.reply_to_message.from_user.mention} has been kicked.")
        except Exception as e:
            await message.reply_text(f"Failed to kick user: {e}")

    @client.on_message(filters.command("mute") & filters.group)
    async def mute_user(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if not message.reply_to_message:
            await message.reply_text("Reply to a user's message to mute them.")
            return
            
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions()
            )
            await message.reply_text(f"User {message.reply_to_message.from_user.mention} has been muted.")
        except Exception as e:
            await message.reply_text(f"Failed to mute user: {e}")

    @client.on_message(filters.command("unmute") & filters.group)
    async def unmute_user(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if not message.reply_to_message:
            await message.reply_text("Reply to a user's message to unmute them.")
            return
            
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            await message.reply_text(f"User {message.reply_to_message.from_user.mention} has been unmuted.")
        except Exception as e:
            await message.reply_text(f"Failed to unmute user: {e}")

    @client.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_message(_, message: Message):
        if message.from_user.id not in config.ADMINS:
            await message.reply_text("You are not authorized to use this command.")
            return
            
        if len(message.command) < 2:
            await message.reply_text("Usage: /broadcast <message>")
            return
            
        broadcast_text = " ".join(message.command[1:])
        # Implement broadcast logic to all groups
        await message.reply_text("Broadcast feature will be implemented here.")
