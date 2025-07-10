import os

class Config:
    API_ID = int(os.getenv("API_ID", "23403968"))
    API_HASH = os.getenv("API_HASH", "494b4d9065307d43a3eb74b57a252a43")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7140094105:AAE7-t9N9xth7i8RdJqW1gPTynAAUcK-MVo")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFlHcAAilJU0f1FsZ3IXjKD18gMkE504tGDi9RegO6tmz5cDVYn2H-xWFZi_LZ37JnYXuGPt4aWXdQaoJjO0vJ4xsgd4JZGQnhLxBDRmp2-nhwJ-u34FXGRhAaCOM9nctHIGhLs3Um2WMi7aq6SwY3qK8dUZcoP-E1ZqNh4hSqHu0i5YbYDlpra_9kAz66GOcpPsSa8Xhg5GMc2J0-Kkm4gLrgKMsp-snumZt_XjhDjNm1wFXsNGkEoR7Lv6Ejzu8EI2NRm5F5lLVlumDF7-Q1-uiI7V_fm4B8M0mpOTIqtVRRe3o5vfAg22k8nkgFZIwTKDvwENwFBuwbt-UIDaybWvnpa-gAAAABjGl6RAA")
    MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://aarubhakar302:effOLpfZ0awCjQxz@cluster0.byhbxty.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1002523753992"))
    
    # Sleep time between song plays (in seconds)
    SLEEP_TIME = int(os.getenv("SLEEP_TIME", "10"))
    
    # Admin user IDs (separate by space)
    ADMINS = list(map(int, os.getenv("ADMINS", "1662672529 1662672529").split()))
    
    # Maximum video quality (0-100)
    MAX_QUALITY = int(os.getenv("MAX_QUALITY", "90"))
    
    # Default volume (0-200)
    DEFAULT_VOLUME = int(os.getenv("DEFAULT_VOLUME", "100"))

config = Config()