from pyrogram import filters, Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback, time
from bot.database.models.user_db import get_admin
from bot.utils.markup import admin_markup, back_markup, empty_markup, promo_button_markup, preview_list_markup
from bot import LOGGER, LOG_CHANNEL
from bot.database.models.post_db import get_buttons, get_post
from bot.database.models.channel_db import get_channel_by_id, chunck, session
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

a = list(chunck())
b = get_post()
p = f"🗣Via @SUPPORT_CHANNEL \n1 hr Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='tg://user?id=SUDO_USERS'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"

# Gestion de la prévisualisation du message promo
@Bot.on_callback_query(filters.regex('^preview$') & filters.user(get_admin()))
async def preview_promo_handler(bot: Client, message: Message):
    LOGGER.info("Handler: preview_promo triggered")
    await bot.send_message(message.message.chat.id, "✅ Choisir la liste de promotion", reply_markup=preview_list_markup())

# Prévisualisation de la promotion classique
@Bot.on_callback_query(filters.regex('^preview_classic_promo$') & filters.user(get_admin()))
async def preview_classic_promo_handler(bot: Client, message: Message):
    LOGGER.info("Handler: preview_classic_promo triggered")
    try:
        for i in a:
            val = ""
            for j in i:
                ch = get_channel_by_id(j)
                val += f'{b.emoji}<a href="{ch.invite_link}">{str(ch.channel_name)}</a>\n'
            dest = b.set_top + "\n\n" + val + "\n" + p + '\n' + b.set_bottom
            await bot.send_message(message.message.chat.id, dest, reply_markup=promo_button_markup(), disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        LOGGER.error(f"Error in preview_classic_promo: {traceback.format_exc()}")
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)

# Prévisualisation de la promotion moderne
@Bot.on_callback_query(filters.regex('^preview_morden_promo$') & filters.user(get_admin()))
async def preview_morden_promo_handler(bot: Client, message: Message):
    LOGGER.info("Handler: preview_morden_promo triggered")
    try:
        for i in a:
            val = ""
            for j in i:
                ch = get_channel_by_id(j)
                val += f'<b>{str(ch.description)}</b>\n{b.emoji}<a href="{ch.invite_link}">「Joιɴ Uѕ」</a>{b.emoji}\n\n'
            dest = b.set_top + "\n" + val + "\n" + p + b.set_bottom
            await bot.send_message(message.message.chat.id, dest, reply_markup=promo_button_markup(), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(f"Error in preview_morden_promo: {traceback.format_exc()}")
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)

# Prévisualisation de la promotion par description
@Bot.on_callback_query(filters.regex('^preview_desc_promo$') & filters.user(get_admin()))
async def preview_desc_promo_handler(bot: Client, message: Message):
    LOGGER.info("Handler: preview_desc_promo triggered")
    try:
        for i in a:
            val = ""
            for j in i:
                ch = get_channel_by_id(j)
                val += f'\n<a href="{ch.invite_link}"><b>{str(ch.description)}</b></a>\n<b>––––––––––––––––––</b>\n\n'
            dest = b.set_top + "\n" + val + "\n" + p + b.set_bottom
            await bot.send_message(message.message.chat.id, dest, reply_markup=promo_button_markup(), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(f"Error in preview_desc_promo: {traceback.format_exc()}")
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)

# Prévisualisation de la promotion avec boutons
@Bot.on_callback_query(filters.regex('^preview_button_promo$') & filters.user(get_admin()))
async def preview_button_promo_handler(bot: Client, message: Message):
    LOGGER.info("Handler: preview_button_promo triggered")
    try:
        down_buttons = get_buttons()
        bq = [InlineKeyboardButton(x.name, url=x.url) for x in down_buttons]
        buttons = []
        for i in a:
            for j in i:
                ch = get_channel_by_id(j)
                buttons.append(InlineKeyboardButton(ch.channel_name, url=ch.invite_link))
            markup = InlineKeyboardMarkup([buttons, bq])
            await bot.send_photo(message.message.chat.id, 'bot/downloads/image.jpg', caption=b.set_caption, reply_markup=markup)
    except Exception as e:
        LOGGER.error(f"Error in preview_button_promo: {traceback.format_exc()}")
        await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
        await bot.send_message(message.message.chat.id, "**⚠️ Un problème est survenu**", parse_mode=enums.ParseMode.MARKDOWN)
