from pyrogram import filters, Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback, time
from bot.database.models.user_db import get_admin, total_admin, total_users
from bot.database.models.channel_db import total_banned_channel, total_channel
from bot.database.models.settings_db import add_list_size, add_subs_limit, get_settings, add_row, get_row
from bot.utils.markup import admin_markup, back_markup, settings_markup, empty_markup
from bot import LOGGER, LOG_CHANNEL, SUDO_USERS


@Bot.on_callback_query(filters.regex('^stats$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def bot_stats(bot: Client, message: Message):
    stats = f"""<b>Total des utilisateurs :</b> {total_users()}
<b>Total des administrateurs :</b> {total_admin()}
<b>Nombre de canaux enregistrés :</b> {total_channel()}
<b>Nombre de canaux bannis :</b> {total_banned_channel()}"""
    LOGGER.info(f"BOT STATISTICS : \n {stats}")
    await bot.send_message(message.message.chat.id, stats)


@Bot.on_callback_query(filters.regex('^settings$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def settings_handler(bot: Client, message: Message):
    info = get_settings()
    
    # Vérification si 'info' est un dictionnaire ou un objet avec des attributs
    if isinstance(info, dict):
        subs_limit = info.get("subs_limit", "Non défini")
        list_size = info.get("list_size", "Non défini")
        row = info.get("row", "Non défini")
    else:
        subs_limit = getattr(info, "subs_limit", "Non défini")
        list_size = getattr(info, "list_size", "Non défini")
        row = getattr(info, "row", "Non défini")
    
    text = f"""
🔄 Limite de abonnés : {subs_limit}
🏷 Taille de la liste : {list_size}
🏷 Nombre de Col : {row}
    """
    await bot.send_message(message.from_user.id, text, reply_markup=settings_markup())


@Bot.on_callback_query(filters.regex('^subs_limit$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def subs_limit_handler(bot: Client, message: Message):
    try:
        data = await bot.ask(message.from_user.id, "Envoyez la limite d'abonnés", reply_markup=back_markup())
        add_subs_limit(int(data.text))
        await bot.send_message(message.from_user.id, "Réglage réussi", reply_markup=empty_markup())
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL, 
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC', 
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.message.chat.id, "<b>❌ Un problème est survenu </b>", reply_markup=empty_markup())


@Bot.on_callback_query(filters.regex('^list_size$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def list_size_handler(bot: Client, message: Message):
    try:
        data = await bot.ask(message.from_user.id, "Envoyez la taille de la liste", reply_markup=back_markup())
        add_list_size(int(data.text))
        await bot.send_message(message.from_user.id, "Réglage réussi", reply_markup=empty_markup())
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL, 
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC', 
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.message.chat.id, "<b>❌ Un problème est survenu</b>", reply_markup=empty_markup())
        
@Bot.on_callback_query(filters.regex('^set_col$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def add_row_handler(bot: Client, message: Message):
    try:
        data = await bot.ask(message.from_user.id, "Envoyez la taille de colonne", reply_markup=back_markup())
        add_row(int(data.text))
        await bot.send_message(message.from_user.id, "Réglage réussi", reply_markup=empty_markup())
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL, 
            f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC', 
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.message.chat.id, "<b>❌ Un problème est survenu</b>", reply_markup=empty_markup())
