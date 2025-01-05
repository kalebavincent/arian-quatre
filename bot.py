import logging
from pyrogram import Client, idle, enums
from config import *
from flask import Flask
import os
from config import *

logging.basicConfig(
    level=logging.WARNING, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("bot.log"),  # Écrit les logs dans bot.log
        logging.StreamHandler()  # Désactivé pour ne pas écrire dans la console
    ]
)

logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running. Made with ♥️ by Hyoshdesign"

def start_server():
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

bot = Client(
    "RenamerBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root='plugins')
)

def main():
    if STRING:
        apps = [bot]
        
        for app_instance in apps:
            app_instance.start()
            logger.warning("Bot started. WARNING and ERROR logs are captured.")
        
        idle()
        
        for app_instance in apps:
            app_instance.stop()
    else:
        bot.run()

if __name__ == "__main__":
    from threading import Thread
    server_thread = Thread(target=start_server)
    server_thread.start()
    
    main()
