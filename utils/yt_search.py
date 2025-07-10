import yt_dlp
import asyncio
from config import config

class YouTubeSearch:
    @staticmethod
    async def search_song(query: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extract_flat': True,
            'noplaylist': True,
            'default_search': 'ytsearch',
            'max_downloads': 1
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, query, download=False)
                
                if 'entries' in info:
                    video = info['entries'][0]
                    return {
                        'title': video.get('title', 'Unknown Title'),
                        'url': video.get('url', ''),
                        'duration': video.get('duration', '0:00'),
                        'views': video.get('view_count', 0)
                    }
                else:
                    return {
                        'title': info.get('title', 'Unknown Title'),
                        'url': info.get('url', ''),
                        'duration': info.get('duration', '0:00'),
                        'views': info.get('view_count', 0)
                    }
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return None

search_song = YouTubeSearch.search_song