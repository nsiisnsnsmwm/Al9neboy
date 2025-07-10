# Vishal Music Bot Setup Guide

## Prerequisites
1. Python 3.8 or higher
2. Telegram API ID and Hash (from https://my.telegram.org)
3. Bot Token (from @BotFather)
4. MongoDB URI (for analytics and data storage)

## Installation
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your configuration (see config.py for required variables)
6. Run the bot: `python main.py`

## Features
- High quality music playback
- Video streaming in voice chats
- Volume control with visual bar
- Progress bar for current song
- Loop mode
- Song queue system
- Admin commands (ban, mute, kick, etc.)
- Spam message feature
- Automatic girlfriend-like replies
- Stylish fonts for all messages
- Welcome messages with sayari for new members

## Note
Make sure to properly configure all environment variables before running the bot.
The bot requires both a bot token and user session string for full functionality.