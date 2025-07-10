import os
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import config
from utils import yt_search, vc_handler
from utils.fonts import apply_font

# Global variables for music control
current_song = None
loop_mode = False
song_queue = []
vc_status = {}

def setup(client: Client, user: Client):
    @client.on_message(filters.command("play") & filters.group)
    async def play_music(_, message: Message):
        global current_song, loop_mode, song_queue
        
        if len(message.command) < 2:
            await message.reply_text("Please provide a song name or YouTube URL.")
            return
            
        query = " ".join(message.command[1:])
        chat_id = message.chat.id
        
        # Check if user is in VC
        if chat_id not in vc_status or not vc_status[chat_id].is_connected:
            # Join VC if not already joined
            try:
                vc = vc_handler.VoiceChat(client, user, chat_id)
                await vc.join()
                vc_status[chat_id] = vc
            except Exception as e:
                await message.reply_text(f"Failed to join voice chat: {e}")
                return
        
        # Search for the song
        try:
            song_info = await yt_search.search_song(query)
            if not song_info:
                await message.reply_text("No results found.")
                return
                
            song_queue.append(song_info)
            
            if current_song is None:
                await play_next_song(chat_id, message)
            else:
                stylish_text = apply_font(f"🎵 Added to queue: {song_info['title']}")
                await message.reply_text(
                    stylish_text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("▶️ Play Now", callback_data=f"playnow_{len(song_queue)-1}")]
                    ])
                )
                
        except Exception as e:
            await message.reply_text(f"Error: {e}")

    async def play_next_song(chat_id, message=None):
        global current_song, loop_mode, song_queue
        
        if chat_id not in vc_status or not vc_status[chat_id].is_connected:
            return
            
        if loop_mode and current_song:
            song = current_song
        elif song_queue:
            song = song_queue.pop(0)
        else:
            current_song = None
            if message:
                await message.reply_text("Queue is empty.")
            return
            
        current_song = song
        
        try:
            vc = vc_status[chat_id]
            await vc.play(song['url'], config.MAX_QUALITY)
            
            stylish_title = apply_font(f"🎶 Now Playing: {song['title']}")
            duration_text = f"⏳ Duration: {song['duration']}"
            views_text = f"👀 Views: {song['views']}"
            
            progress_bar = await create_progress_bar(0, 10)
            volume_bar = await create_volume_bar(config.DEFAULT_VOLUME)
            
            if message:
                await message.reply_text(
                    f"{stylish_title}\n{duration_text}\n{views_text}\n\n{progress_bar}\n{volume_bar}",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("⏮", callback_data="previous"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="next"),
                            InlineKeyboardButton("🔁" if loop_mode else "🔂", callback_data="loop")
                        ],
                        [
                            InlineKeyboardButton("🔈", callback_data="vol_down"),
                            InlineKeyboardButton("🔊", callback_data="vol_up"),
                            InlineKeyboardButton("❌", callback_data="stop")
                        ]
                    ])
                )
                
            # Sleep time between songs
            await asyncio.sleep(config.SLEEP_TIME)
            await play_next_song(chat_id)
            
        except Exception as e:
            await message.reply_text(f"Error playing song: {e}")
            current_song = None
            await play_next_song(chat_id)

    async def create_progress_bar(progress, total):
        filled = int(progress / total * 10)
        empty = 10 - filled
        return "[" + "■" * filled + "□" * empty + "]"

    async def create_volume_bar(volume):
        filled = int(volume / 200 * 10)
        empty = 10 - filled
        return "Volume: [" + "■" * filled + "□" * empty + f"] {volume}%"

    @client.on_callback_query(filters.regex(r"^playnow_"))
    async def play_now_callback(_, query):
        index = int(query.data.split("_")[1])
        if 0 <= index < len(song_queue):
            song_queue.insert(0, song_queue.pop(index))
            await query.answer("Song will play next!")
            await play_next_song(query.message.chat.id, query.message)
        else:
            await query.answer("Invalid song index!")

    @client.on_callback_query(filters.regex(r"^(previous|pause|next|loop|vol_down|vol_up|stop)$"))
    async def control_callback(_, query):
        global loop_mode
        
        chat_id = query.message.chat.id
        vc = vc_status.get(chat_id)
        
        if not vc or not vc.is_connected:
            await query.answer("Not connected to voice chat!")
            return
            
        if query.data == "previous":
            await query.answer("Playing previous song...")
            # Implement previous song logic
        elif query.data == "pause":
            if vc.is_paused:
                await vc.resume()
                await query.answer("Resumed playback")
            else:
                await vc.pause()
                await query.answer("Paused playback")
        elif query.data == "next":
            await query.answer("Playing next song...")
            await play_next_song(chat_id)
        elif query.data == "loop":
            loop_mode = not loop_mode
            await query.answer(f"Loop mode {'enabled' if loop_mode else 'disabled'}")
        elif query.data == "vol_down":
            new_vol = max(0, vc.volume - 10)
            await vc.set_volume(new_vol)
            await query.answer(f"Volume decreased to {new_vol}%")
        elif query.data == "vol_up":
            new_vol = min(200, vc.volume + 10)
            await vc.set_volume(new_vol)
            await query.answer(f"Volume increased to {new_vol}%")
        elif query.data == "stop":
            await vc.stop()
            await query.answer("Playback stopped")
            current_song = None
            song_queue.clear()
            
        # Update the message with new controls
        if query.data in ["pause", "loop", "vol_down", "vol_up"]:
            progress_bar = await create_progress_bar(5, 10)  # Example progress
            volume_bar = await create_volume_bar(vc.volume if vc else config.DEFAULT_VOLUME)
            
            await query.message.edit_reply_markup(
                InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("⏮", callback_data="previous"),
                        InlineKeyboardButton("⏸" if not vc.is_paused else "▶", callback_data="pause"),
                        InlineKeyboardButton("⏭", callback_data="next"),
                        InlineKeyboardButton("🔁" if loop_mode else "🔂", callback_data="loop")
                    ],
                    [
                        InlineKeyboardButton("🔈", callback_data="vol_down"),
                        InlineKeyboardButton("🔊", callback_data="vol_up"),
                        InlineKeyboardButton("❌", callback_data="stop")
                    ]
                ])
            )

    @client.on_message(filters.command("queue") & filters.group)
    async def show_queue(_, message: Message):
        if not song_queue:
            await message.reply_text("Queue is empty.")
            return
            
        queue_text = "🎵 Current Queue:\n"
        for i, song in enumerate(song_queue[:10], 1):
            queue_text += f"{i}. {song['title']} ({song['duration']})\n"
            
        if len(song_queue) > 10:
            queue_text += f"\nAnd {len(song_queue) - 10} more songs..."
            
        await message.reply_text(queue_text)

    @client.on_message(filters.command("loop") & filters.group)
    async def toggle_loop(_, message: Message):
        global loop_mode
        loop_mode = not loop_mode
        await message.reply_text(f"Loop mode is now {'enabled' if loop_mode else 'disabled'}.")

    @client.on_message(filters.command("leave") & filters.group)
    async def leave_vc(_, message: Message):
        chat_id = message.chat.id
        if chat_id in vc_status:
            await vc_status[chat_id].leave()
            del vc_status[chat_id]
            await message.reply_text("Left the voice chat.")
        else:
            await message.reply_text("Not in a voice chat.")

    @client.on_message(filters.command("now") & filters.group)
    async def now_playing(_, message: Message):
        if current_song:
            stylish_text = f"🎶 Now Playing: {current_song['title']}\n"
            stylish_text += f"⏳ Duration: {current_song['duration']}\n"
            stylish_text += f"👀 Views: {current_song['views']}"
            await message.reply_text(stylish_text)
        else:
            await message.reply_text("No song is currently playing.")