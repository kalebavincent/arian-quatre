import asyncio
from pyrogram import Client, __version__
from config import Config
from aiohttp import web
from route import web_server
import time

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="Crypto_mine",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        self.start_time = time.time()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", 8080).start()
        print(f"{me.first_name} Is Started.....✨️")

    async def stop(self):
        await super().stop()

async def main():
    bot = Bot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
