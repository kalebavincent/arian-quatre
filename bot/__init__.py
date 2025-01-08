# -*-coding : utf-8 -*-
from datetime import datetime
from importlib import import_module as imp_mod
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger, DEBUG
from os import environ, mkdir, path
from sys import exit as sysexit
from sys import stdout, version_info
from time import time
from traceback import format_exc
from bot.config import Config
import asyncio
from flask import Flask, jsonify

LOG_DATETIME = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")

stdout_handler = StreamHandler(stdout)

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=INFO,
    handlers=[stdout_handler],
)

getLogger("pyrogram").setLevel(INFO)
getLogger('sqlalchemy.engine').setLevel(INFO)

LOGGER = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 7:
    LOGGER.error(
        (
            "You MUST have a Python Version of at least 3.7!\n"
            "Multiple features depend on this. Bot quitting."
        ),
    )
    sysexit(1)

STRING_SESSION = Config.STRING_SESSION
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
SUPPORT_GROUP = Config.SUPPORT_GROUP
SUPPORT_CHANNEL = Config.SUPPORT_CHANNEL
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
DATABASE_URI = Config.DATABASE_URI
WORKERS = Config.WORKERS
BOT_TOKEN = Config.BOT_TOKEN
PREFIX_HANDLER = Config.PREFIX_HANDLER
PROMOTION_NAME = Config.PROMOTION_NAME
VERSION = Config.VERSION
UPTIME = time()
BOT_USERNAME = ""
BOT_NAME = ""
BOT_ID = 0

from bot.database import session, base
from bot.database.models.user_db import add_admin, get_admin

def add_admin_if_not_exists(user_chat_id):
    existing_admins = get_admin()
    if user_chat_id in existing_admins:
        print(f"User with chat_id {user_chat_id} is already an admin.")
    else:
        add_admin(user_chat_id)
        print(f"Added user with chat_id {user_chat_id} as admin.")

user_chat_id = SUDO_USERS
if user_chat_id:
    add_admin_if_not_exists(user_chat_id)

# Flask server setup
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """ Endpoint to check if the server is alive. """
    return jsonify({"status": "ok", "message": "Server is running."}), 200

def run_flask():
    """ Fonction pour lancer le serveur Flask sur le port 5000. """
    app.run(host='0.0.0.0', port=5000, debug=False)

# Lancer le serveur Flask dans un thread séparé
from threading import Thread

flask_thread = Thread(target=run_flask)
flask_thread.start()
