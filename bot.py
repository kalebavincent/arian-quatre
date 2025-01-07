from flask import Flask, jsonify
import threading
import asyncio
from platform import python_version
from time import gmtime, strftime, time
from pyrogram import Client, __version__, enums
from pyrogram.raw.all import layer
from bot.database import session, base
from bot import (
    STRING_SESSION,
    API_HASH,
    APP_ID,
    LOG_CHANNEL,
    LOG_DATETIME,
    LOGGER,
    STRING_SESSION,
    WORKERS,
    UPTIME,
    BOT_TOKEN)

app = Flask(__name__)

# Variable globale pour savoir si le bot est en ligne
bot_online = False

class Bot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            STRING_SESSION,
            plugins=dict(root=f"{name}.plugins"),
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=WORKERS,
            parse_mode=enums.ParseMode.HTML
        )
        
    async def start(self):
        global bot_online
        await super().start() 
        LOGGER.info("Starting bot...")

        me = await self.get_me()  
        LOGGER.info(
            f"Pyrogram v{__version__} (Layer - {layer}) started on {me.username} [{me.id}]",
        )
        LOGGER.info(f"Python Version: {python_version()}\n")
        LOGGER.info("Bot Started Successfully!\n")
        await asyncio.sleep(60)
        await self.send_message(LOG_CHANNEL, "<i>Démarrage du bot...</i>")
        
        bot_online = True  # Marquer le bot comme étant en ligne

    async def stop(self):
        global bot_online
        runtime = strftime("%Hh %Mm %Ss", gmtime(time() - UPTIME))
        LOGGER.info("Uploading logs before stopping...!\n")
        await self.send_message(
            LOG_CHANNEL,
            ("Bot arrêté!\n\n"
             f"Temps d'exécution: {runtime}\n"
             f"<code>{LOG_DATETIME}</code>")
        )

        await super().stop()
        LOGGER.info(
            f"""Bot arrêté [Temps d'exécution: {runtime}s]\n"""
        )   
        bot_online = False  # Marquer le bot comme arrêté

# Route Flask pour vérifier si le bot est en ligne
@app.route("/check_live", methods=["GET"])
def check_live():
    if bot_online:
        return jsonify({"status": "Bot is online"}), 200
    else:
        return jsonify({"status": "Bot is offline"}), 503

# Fonction pour démarrer Flask dans un thread séparé
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)

# Démarrer le bot et le serveur Flask dans des threads séparés
def start_bot_and_flask():
    bot = Bot()

    # Lancer Flask dans un thread séparé
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Démarrer le bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start())

if __name__ == "__main__":
    start_bot_and_flask()
