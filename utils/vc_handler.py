import os
import ffmpeg
from pyrogram import Client
from pyrogram.types import Message
from config import config

class VoiceChat:
    def __init__(self, bot: Client, user: Client, chat_id: int):
        self.bot = bot
        self.user = user
        self.chat_id = chat_id
        self.is_connected = False
        self.is_playing = False
        self.is_paused = False
        self.volume = config.DEFAULT_VOLUME
        self.current_stream = None
        
    async def join(self):
        if self.is_connected:
            return True
            
        try:
            await self.user.send_message(self.chat_id, "/joinvc")
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Error joining voice chat: {e}")
            return False
            
    async def leave(self):
        if not self.is_connected:
            return True
            
        try:
            await self.user.send_message(self.chat_id, "/leavevc")
            self.is_connected = False
            self.is_playing = False
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Error leaving voice chat: {e}")
            return False
            
    async def play(self, url: str, quality: int = 90):
        if not self.is_connected:
            if not await self.join():
                return False
                
        try:
            # Download the audio stream with specified quality
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'opus',
                    'preferredquality': str(quality)
                }],
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                audio_file = os.path.splitext(filename)[0] + '.opus'
                
            # Play the audio file
            await self.user.send_audio(
                self.chat_id,
                audio_file,
                volume=self.volume
            )
            
            # Clean up
            os.remove(audio_file)
            self.is_playing = True
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
            
    async def pause(self):
        if not self.is_connected or not self.is_playing:
            return False
            
        try:
            await self.user.send_message(self.chat_id, "/pause")
            self.is_paused = True
            return True
        except Exception as e:
            print(f"Error pausing playback: {e}")
            return False
            
    async def resume(self):
        if not self.is_connected or not self.is_paused:
            return False
            
        try:
            await self.user.send_message(self.chat_id, "/resume")
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Error resuming playback: {e}")
            return False
            
    async def stop(self):
        if not self.is_connected:
            return False
            
        try:
            await self.user.send_message(self.chat_id, "/stop")
            self.is_playing = False
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Error stopping playback: {e}")
            return False
            
    async def set_volume(self, volume: int):
        if not self.is_connected:
            return False
            
        try:
            await self.user.send_message(self.chat_id, f"/volume {volume}")
            self.volume = volume
            return True
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False

# Global VC status tracker
vc_status = {}

def get_vc(chat_id: int, bot: Client, user: Client):
    if chat_id not in vc_status:
        vc_status[chat_id] = VoiceChat(bot, user, chat_id)
    return vc_status[chat_id]