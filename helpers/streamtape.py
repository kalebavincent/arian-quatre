import aiohttp
from configs import Config
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.display_progress import humanbytes


async def UploadToStreamtape(file: str, editable: Message, file_size: int):
    try:
        async with aiohttp.ClientSession() as session:
            Main_API = "https://api.streamtape.com/file/ul?login={}&key={}"
            hit_api = await session.get(Main_API.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS))
            json_data = await hit_api.json()
            temp_api = json_data["result"]["url"]
            files = {'file1': open(file, 'rb')}
            response = await session.post(temp_api, data=files)
            data_f = await response.json(content_type=None)
            download_link = data_f["result"]["url"]
            filename = file.split("/")[-1].replace("_", " ")
            
            text_edit = f"📤 **ꜰɪᴄʜɪᴇʀ ᴛéʟéᴠᴇʀꜱé ꜱᴜʀ ꜱᴛʀᴇᴀᴍᴛᴀᴘᴇ !**\n\n" \
                        f"📂 **ɴᴏᴍ ᴅᴜ ꜰɪᴄʜɪᴇʀ:** `{filename}`\n" \
                        f"📊 **ᴛᴀɪʟʟᴇ :** `{humanbytes(file_size)}`\n" \
                        f"🔗 **ʟɪᴇɴ ᴅᴇ ᴛéʟéᴄʜᴀʀɢᴇᴍᴇɴᴛ :** [ᴄʟɪQᴜᴇᴢ ɪᴄɪ]({download_link})"
            
            await editable.edit(text_edit, parse_mode="Markdown", disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("🔗 ᴏᴜᴠʀɪʀ ʟᴇ ʟɪᴇɴ", url=download_link)]
                                ]))
    except Exception as e:
        print(f"Erreur : {e}")
        await editable.edit("❌ ᴅéꜱᴏʟé, QᴜᴇʟQᴜᴇ ᴄʜᴏꜱᴇ ꜱ'ᴇꜱᴛ ᴍᴀʟ ᴘᴀꜱꜱé !\n\n" 
                            "ɪᴍᴘᴏꜱꜱɪʙʟᴇ ᴅᴇ ᴛéʟéᴠᴇʀꜱᴇʀ ꜱᴜʀ ꜱᴛʀᴇᴀᴍᴛᴀᴘᴇ. ᴠᴏᴜꜱ ᴘᴏᴜᴠᴇᴢ ꜱɪɢɴᴀʟᴇʀ ʟᴇ ᴘʀᴏʙʟèᴍᴇ ᴀ ɴᴏᴛʀᴇ" 
                            "[ᴀᴅᴍɪɴꜱᴛʀᴀᴛᴇᴜʀ](https://t.me/hyoshdesign).")
