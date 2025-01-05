import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
OWNER = int(os.getenv("OWNER", ""))
BOT_USERNAME = os.getenv('BOT_USERNAME', "")
STRING = os.getenv("STRING", "")
