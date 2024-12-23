import os
from dotenv import load_dotenv
load_dotenv()
class Config(object):
    # API and Authentication
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    BOT_OWNER = int(os.environ.get("BOT_OWNER" , 5814104129))

    # Session and Channels
    SESSION_NAME = os.environ.get("SESSION_NAME", "Video-Merge-Bot")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL")
    LOG_CHANNEL = os.environ.get("LOG_CHANNEL")

    # File Handling
    DOWN_PATH = os.environ.get("DOWN_PATH", "./downloads")
    MAX_VIDEOS = int(os.environ.get("MAX_VIDEOS", 5))
    IMG_FOLDER = os.environ.get("IMG_FOLDER", "./img")

    # Streamtape Integration
    STREAMTAPE_API_USERNAME = os.environ.get("STREAMTAPE_API_USERNAME")
    STREAMTAPE_API_PASS = os.environ.get("STREAMTAPE_API_PASS")

    # MongoDB
    MONGODB_URI = os.environ.get("MONGODB_URI")

    # Miscellaneous
    TIME_GAP = int(os.environ.get("TIME_GAP", 5))
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))

    # Text and Captions
    START_TEXT = """
    ꜱᴀʟᴜᴛ 👋, ᴊᴇ ꜱᴜɪꜱ ᴜɴ ʙᴏᴛ ᴅᴇ ꜰᴜꜱɪᴏɴ ᴅᴇ ᴠɪᴅéᴏꜱ !
ᴊᴇ ᴘᴇᴜx ꜰᴜꜱɪᴏɴɴᴇʀ ᴘʟᴜꜱɪᴇᴜʀꜱ ᴠɪᴅéᴏꜱ ᴇɴ ᴜɴᴇ ꜱᴇᴜʟᴇ. ʟᴇꜱ ꜰᴏʀᴍᴀᴛꜱ ᴠɪᴅéᴏ ᴅᴏɪᴠᴇɴᴛ êᴛʀᴇ ɪᴅᴇɴᴛɪQᴜᴇꜱ
    """
    CAPTION = "ᴠɪᴅᴇᴏ ᴍᴇʀɢᴇᴅ ʙʏ @{}\n\nᴍᴀᴅᴇ ʙʏ @hyoshdesign"

    # Progress Text
    PROGRESS = """
    🟢 **ᴘᴏᴜʀᴄᴇɴᴛᴀɢᴇ** : {0}%
    🔹 **ᴛᴇʀᴍɪɴé** : {1}
    🔸 **ᴛᴏᴛᴀʟ** : {2}
    ⚡ **ᴠɪᴛᴇꜱꜱᴇ** : {3}/s
    ⏳ **ᴛᴇᴍᴘꜱ ᴇꜱᴛɪᴍé ʀᴇꜱᴛᴀɴᴛ** : {4}
    """
