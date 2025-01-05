import re, os, time
from os import environ, getenv
from dotenv import load_dotenv
load_dotenv()
id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")

    PORT = os.getenv("PORT", 8000)  
    WEBHOOK = bool(os.getenv("WEBHOOK"))
