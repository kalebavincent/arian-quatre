from pyrogram import filters, Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback, time
from bot.database.models.user_db import get_admin
from bot.utils.markup import admin_markup, back_markup, empty_markup, promo_button_markup, preview_list_markup
from bot import LOGGER, LOG_CHANNEL
from bot.database.models.post_db import get_buttons, get_post
from bot.database.models.settings_db import get_row, get_settings
from bot.database.models.channel_db import get_channel_by_id, chunck, session
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Préparation des données
a = list(chunck())
b = get_post()
p = f"🗣Via @SUPPORT_CHANNEL \n1 hr Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='tg://user?id=SUDO_USERS'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"

# Fonction de gestion des erreurs générales
async def handle_error(exception, bot: Client, message: Message, custom_message: str):
    error_message = traceback.format_exc()
    LOGGER.error(f"Exception: {error_message}")
    await bot.send_message(LOG_CHANNEL, f'\n<code>{error_message}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
    await bot.send_message(message.message.chat.id, f"**⚠️ {custom_message}**\n\nDétails de l'erreur envoyés aux administrateurs.", parse_mode=enums.ParseMode.MARKDOWN)

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
        await handle_error(e, bot, message, "Un problème est survenu lors de la prévisualisation classique.")

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
        await handle_error(e, bot, message, "Un problème est survenu lors de la prévisualisation moderne.")

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
        await handle_error(e, bot, message, "Un problème est survenu lors de la prévisualisation par description.")

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
        await handle_error(e, bot, message, "Un problème est survenu lors de la prévisualisation avec boutons.")


@Bot.on_callback_query(filters.regex('^preview_with_dynamic_columns$') & filters.user(get_admin()))
async def preview_with_dynamic_columns_handler(bot: Client, message: Message):
    LOGGER.info("Handler: preview_with_dynamic_columns triggered")
    try:        
        info = get_settings()
        if isinstance(info, dict):
            rows = info.get("row", "Non défini")
            max_col = rows
        else :
            rows = getattr(info, "row", "Non défini")
            max_col = rows
            
        max_buttons_per_message = 20  # Nombre maximal de boutons par message
        buttons = []

        # Récupérer la liste des canaux et créer des boutons
        for i in a:  # Assumons que 'a' contient les IDs des canaux
            for j in i:
                ch = get_channel_by_id(j)  # Récupère le canal à partir de la base de données
                if ch:  # Vérifie si le canal existe
                    button = InlineKeyboardButton(ch.channel_name, url=ch.invite_link)
                    buttons.append(button)

        # Calculer dynamiquement le nombre de colonnes
        total_buttons = len(buttons)
        col = min(max_col, max(1, total_buttons // 2))  # S'assurer qu'il y a au moins 1 colonne et ajuster selon la taille des boutons

        # Organiser les boutons en lignes et colonnes
        button_rows = [buttons[i:i + col] for i in range(0, total_buttons, col)]

        # Si le nombre de boutons est trop grand, découper les messages pour ne pas dépasser la limite
        # de Telegram pour le nombre de boutons.
        message_text = f"<b>Voici la liste des canaux :</b>\n\n{p}"
        
        # Envoi des messages avec le nombre correct de boutons
        for row in button_rows:
            markup = InlineKeyboardMarkup([row])
            await bot.send_message(
                message.message.chat.id, 
                message_text, 
                reply_markup=markup, 
                parse_mode=enums.ParseMode.HTML
            )
            # Vous pouvez ajouter un délai entre chaque envoi de message si nécessaire pour éviter des erreurs avec un grand nombre de boutons.

    except Exception as e:
        await handle_error(e, bot, message, "Un problème est survenu lors de la prévisualisation avec colonnes dynamiques.")
