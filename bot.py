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
        # Initialize the bot's start time for uptime calculation
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

        # # Calculate uptime using timedelta
        # uptime_seconds = int(time.time() - self.start_time)
        # uptime_string = str(timedelta(seconds=uptime_seconds))

        # # Envoi d'un message dans les canaux/logs
        # try:
        #     curr = datetime.now(timezone("Asia/Kolkata"))
        #     date = curr.strftime('%d %B, %Y')
        #     time_str = curr.strftime('%I:%M:%S %p')

        #     # Send the message with the photo
        #     await self.send_photo(
        #         chat_id=SUPPORT_CHAT,
        #         photo=Config.START_PIC,
        #         caption=(
        #             "**ᴀɴʏᴀ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ  !**\n\n"
        #             f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​: `{uptime_string}`"
        #         ),
        #         reply_markup=InlineKeyboardMarkup(
        #             [[
        #                 InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/codeflix_bots")
        #             ]]
        #         )
        #     )
        # except Exception as e:
        #     print(f"Failed to send message in chat {SUPPORT_CHAT}: {e}")

Bot().run()
