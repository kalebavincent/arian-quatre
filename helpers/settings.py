import asyncio
from helpers.database.access_db import db
from pyrogram.errors import MessageNotModified, FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def OpenSettings(m: Message, user_id: int):
    try:
        await m.edit(
            text="⚙️ **ᴘᴀʀᴀᴍèᴛʀᴇꜱ ᴅᴇ ᴠᴏᴛʀᴇ ᴄᴏᴍᴘᴛᴇ** :\n\nɪᴄɪ, ᴠᴏᴜꜱ ᴘᴏᴜᴠᴇᴢ ᴄᴏɴꜰɪɢᴜʀᴇʀ ᴠᴏꜱ ᴘʀéꜰéʀᴇɴᴄᴇꜱ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(f"📹 ᴛéʟéᴄʜᴀʀɢᴇʀ ᴇɴ ᴛᴀɴᴛ Qᴜᴇ {'ᴠɪᴅéᴏ' if (await db.get_upload_as_doc(id=user_id)) is False else 'ᴅᴏᴄᴜᴍᴇɴᴛ'} ✅", callback_data="triggerUploadMode")],
                    [InlineKeyboardButton(f"🎬 ɢéɴéʀᴇʀ ᴜɴᴇ ᴠɪᴅéᴏ ᴅ'ᴇxᴇᴍᴘʟᴇ {'✅' if (await db.get_generate_sample_video(id=user_id)) is True else '❌'}", callback_data="triggerGenSample")],
                    [InlineKeyboardButton(f"📸 ɢéɴéʀᴇʀ ᴅᴇꜱ ᴄᴀᴘᴛᴜʀᴇꜱ ᴅ'éᴄʀᴀɴ {'✅' if (await db.get_generate_ss(id=user_id)) is True else '❌'}", callback_data="triggerGenSS")],
                    [InlineKeyboardButton("🌄 ᴀꜰꜰɪᴄʜᴇʀ ʟᴀ ᴍɪɴɪᴀᴛᴜʀᴇ", callback_data="showThumbnail")],
                    [InlineKeyboardButton("🗂️ ᴀꜰꜰɪᴄʜᴇʀ ʟᴇꜱ ꜰɪᴄʜɪᴇʀꜱ ᴇɴ ᴀᴛᴛᴇɴᴛᴇ", callback_data="showQueueFiles")],
                    [InlineKeyboardButton("❌ ꜰᴇʀᴍᴇʀ", callback_data="closeMeh")]
                ]
            )
        )
    except MessageNotModified:
        pass
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await m.edit("⏳ ᴠᴏᴜꜱ êᴛᴇꜱ ᴇɴ ᴛʀᴀɪɴ ᴅᴇ ꜱᴘᴀᴍᴇʀ ! ᴠᴇᴜɪʟʟᴇᴢ ᴘᴀᴛɪᴇɴᴛᴇʀ.")
    except Exception as err:
        raise err
