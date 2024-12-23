import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def ForceSub(bot: Client, cmd: Message):
    try:
        chat_id = int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
    except Exception as err:
        print(f"ɪᴍᴘᴏꜱꜱɪʙʟᴇ ᴅᴇ ᴄᴏɴꜰɪɢᴜʀᴇʀ ʟᴇ ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ᴘᴏᴜʀ{Config.UPDATES_CHANNEL}\nErreur : {err}")
        return 200

    try:
        user = await bot.get_chat_member(chat_id=chat_id, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="ᴅéꜱᴏʟé, ᴠᴏᴜꜱ êᴛᴇꜱ ʙᴀɴɴɪ ᴅᴇ ʟ'ᴜᴛɪʟɪꜱᴀᴛɪᴏɴ ᴅᴇ ᴄᴇ ʙᴏᴛ. ᴠᴇᴜɪʟʟᴇᴢ ᴄᴏɴᴛᴀᴄᴛᴇʀ ᴍᴏɴ [ᴀᴅᴍɪɴꜱᴛʀᴀᴛᴇᴜʀ](https://t.me/hyoshdesign).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text=(
                "**ᴠᴇᴜɪʟʟᴇᴢ ʀᴇᴊᴏɪɴᴅʀᴇ ᴍᴏɴ ᴄᴀɴᴀʟ ᴅᴇ ᴍɪꜱᴇꜱ à ᴊᴏᴜʀ ᴘᴏᴜʀ ᴜᴛɪʟɪꜱᴇʀ ᴄᴇ ʙᴏᴛ !**\n\n"
                "ᴇɴ ʀᴀɪꜱᴏɴ ᴅ'ᴜɴᴇ ꜱᴜʀᴄʜᴀʀɢᴇ, ꜱᴇᴜʟꜱ ʟᴇꜱ ᴀʙᴏɴɴéꜱ ᴀᴜ ᴄᴀɴᴀʟ ᴘᴇᴜᴠᴇɴᴛ ᴜᴛɪʟɪꜱᴇʀ ᴄᴇ ʙᴏᴛ."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🤖 ʀᴇᴊᴏɪɴᴅʀᴇ ʟᴇ ᴄᴀɴᴀʟ ᴅᴇ ᴍɪꜱᴇꜱ à ᴊᴏᴜʀ", url=invite_link.invite_link)],
                    [InlineKeyboardButton("🔄 ʀᴀꜰʀᴀîᴄʜɪʀ 🔄", callback_data="refreshFsub")]
                ]
            ),
            parse_mode="markdown"
        )
        return 400
    except Exception as e:
        print(f"ᴇʀʀᴇᴜʀ ɪɴᴄᴏɴɴᴜᴇ ʟᴏʀꜱ ᴅᴇ ʟᴀ ᴠéʀɪꜰɪᴄᴀᴛɪᴏɴ ᴅ'ᴀʙᴏɴɴᴇᴍᴇɴt : {e}")
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="ᴜɴᴇ ᴇʀʀᴇᴜʀ ᴇꜱᴛ ꜱᴜʀᴠᴇɴᴜᴇ. ᴠᴇᴜɪʟʟᴇᴢ ᴄᴏɴᴛᴀᴄᴛᴇʀ ᴍᴏɴ [ᴀᴅᴍɪɴꜱᴛʀᴀᴛᴇᴜʀ](https://t.me/hyoshdesign).",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
        return 400

    return 200
