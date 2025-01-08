import re
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.bot import Bot
from bot.database.models.channel_db import get_all_channels
from bot.database.models.promo_db import save_message_ids, get_promo, delete_promo
from bot import LOGGER, LOG_CHANNEL, SUDO_USERS

# Commandes supportées
COMMAND_REGEX = r"^/(send|s)\s+\{(?P<message>.+?)\}\s*(notto\s+\{(?P<exclude>.+?)\})?\s*(at\s+(?P<time>\d{1,2}:\d{2}(am|pm)?))?\s*(for\s+(?P<duration>\d+)(min|hours))?\s*(until\s+(?P<until_time>\d{1,2}:\d{2}(am|pm)?))?$"

@Bot.on_message(filters.command(["send", "s"]) & filters.user(SUDO_USERS))
async def send_command_handler(bot: Client, message: Message):
    """Gère l'envoi des messages selon les paramètres fournis."""
    try:
        command = message.text
        match = re.match(COMMAND_REGEX, command)
        if not match:
            await message.reply_text(
                "❌ Format invalide. Utilisez :\n`/send {message} [notto {channels}] [at time] [for X hours/min] [until time]`",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return

        # Extraction des paramètres
        promo_message = match.group("message").strip()
        exclude_channels = match.group("exclude")
        time_to_send = match.group("time")
        duration = match.group("duration")
        duration_unit = match.group(9)  # min ou hours
        until_time = match.group("until_time")

        # Conversion des exclusions en liste
        exclude_list = []
        if exclude_channels:
            exclude_list = [x.strip() for x in exclude_channels.split(",")]

        # Récupération des canaux enregistrés
        channels = get_all_channels()
        if not channels:
            await message.reply_text("❌ Aucun canal enregistré.")
            return

        # Filtrage des canaux exclus
        target_channels = [channel for channel in channels if channel.channel_id not in exclude_list]

        # Envoi immédiat
        sent_message_ids = []
        for channel in target_channels:
            try:
                sent_message = await bot.send_message(
                    chat_id=channel.channel_id,
                    text=promo_message,
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                save_message_ids(channel.channel_id, sent_message.message_id)
                sent_message_ids.append((channel.channel_id, sent_message.message_id))
            except Exception as e:
                LOGGER.error(f"Erreur lors de l'envoi au canal {channel.channel_name} : {e}")
                await message.reply_text(f"❌ Erreur lors de l'envoi au canal {channel.channel_name} : {str(e)}")

        # Message de confirmation avec boutons
        if sent_message_ids:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Effacer", callback_data=f"delete_promo:{sent_message_ids}"),
                 InlineKeyboardButton("🔄 Renvoyer", callback_data=f"resend_promo:{sent_message_ids}")]
            ])
            await message.reply_text(
                f"✅ Message envoyé avec succès dans {len(sent_message_ids)} canaux.",
                reply_markup=buttons
            )
        else:
            await message.reply_text("❌ Aucun message n'a été envoyé.")

        # Programmation ou suppression différée
        if time_to_send or duration or until_time:
            # Implémenter la logique pour gérer les délais et suppressions
            LOGGER.info("Programmation ou suppression différée à implémenter.")
    except Exception as e:
        LOGGER.error(f"Erreur lors de la commande /send : {e}")
        await message.reply_text("❌ Une erreur s'est produite lors de l'exécution de la commande.")


@Bot.on_callback_query(filters.regex(r"^(delete_promo|resend_promo):"))
async def callback_handler(bot: Client, query):
    """Gère les actions des boutons."""
    try:
        action, sent_message_ids = query.data.split(":")
        sent_message_ids = eval(sent_message_ids)  # Convertir la chaîne en liste

        if action == "delete_promo":
            for channel_id, message_id in sent_message_ids:
                try:
                    await bot.delete_messages(chat_id=channel_id, message_ids=message_id)
                except Exception as e:
                    LOGGER.error(f"Erreur lors de la suppression du message {message_id} dans {channel_id} : {e}")
            delete_promo()
            await query.message.edit_text("✅ Tous les messages ont été supprimés.")

        elif action == "resend_promo":
            for channel_id, message_id in sent_message_ids:
                try:
                    original_message = await bot.get_messages(chat_id=channel_id, message_ids=message_id)
                    await bot.send_message(
                        chat_id=channel_id,
                        text=original_message.text,
                        parse_mode=enums.ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                except Exception as e:
                    LOGGER.error(f"Erreur lors du renvoi dans {channel_id} : {e}")
            await query.message.edit_text("✅ Messages renvoyés avec succès.")

    except Exception as e:
        LOGGER.error(f"Erreur lors de la gestion des actions des boutons : {e}")
        await query.message.reply_text("❌ Une erreur s'est produite.")
