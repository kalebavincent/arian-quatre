from pyrogram import filters, Client, enums
from pyrogram.types import Message
import traceback, time
from bot import LOGGER, LOG_CHANNEL, SUDO_USERS, SUPPORT_GROUP
from bot.bot import Bot
from bot.database.models.channel_db import is_channel_ban, is_channel_exist, channel_data
from bot.utils.markup import start_markup, back_markup, empty_markup
from bot.utils.is_admin import is_bot_admin
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, ChannelPrivate
from bot.database.models.settings_db import get_subcribers_limit

@Bot.on_callback_query(filters.regex('^add_channel$'))
async def add_channel(bot: Client, message: Message):
    try:
        # Demander un transfert de message pour obtenir les informations du canal
        channel = await bot.ask(
            message.message.chat.id,
            "✅ <b>Faites de ce bot un administrateur et transférez le message depuis le canal</b>",
            reply_markup=back_markup()
        )
        
        # Annulation par l'utilisateur
        if channel.text == '🚫 Cancel':
            await bot.send_message(message.message.chat.id, "🚫 <b>Annulé</b>", reply_markup=empty_markup())
            return
        
        # Vérification du message transféré
        if not channel.forward_from_chat:
            await bot.send_message(message.message.chat.id, "❌ <b>Message invalide. Veuillez transférer un message valide depuis un canal.</b>", reply_markup=empty_markup())
            return
        
        chat_id = message.from_user.id
        channel_id = channel.forward_from_chat.id
        channel_name = channel.forward_from_chat.title

        # Vérifier si le canal est banni ou déjà enregistré
        if is_channel_ban(channel_id):
            await bot.send_message(chat_id, "❌ <b>Ce canal est banni.</b>", reply_markup=empty_markup())
            return

        if is_channel_exist(channel_id):
            await bot.send_message(chat_id, "❌ <b>Ce canal existe déjà dans la base de données.</b>", reply_markup=empty_markup())
            return

        # Vérification si le bot est administrateur
        if not await is_bot_admin(bot, channel_id):
            await bot.send_message(chat_id, "❌ <b>Le bot n'est pas administrateur dans ce canal.</b>", reply_markup=empty_markup())
            return

        # Vérifier le nombre d'abonnés
        limit = get_subcribers_limit()
        chat_info = await bot.get_chat(channel_id)
        subscribers = chat_info.members_count

        if subscribers < limit:
            await bot.send_message(chat_id, f"❌ <b>Vous avez besoin d'au moins {limit} abonnés pour enregistrer ce canal.</b>", reply_markup=empty_markup())
            return

        # Demander une description
        description = await bot.ask(chat_id, "<b>✅ Envoyez une description (maximum 5 mots et 2 emojis)</b>", reply_markup=empty_markup())
        admin_username = message.from_user.username
        invite_link = await bot.export_chat_invite_link(channel_id)

        # Ajouter le canal à la base de données
        channel_data(chat_id, channel_id, channel_name, subscribers, admin_username, description.text, invite_link)
        details = (
            f"✅ <b>Canal soumis avec succès</b>\n\n"
            f"🆔 ID : {channel_id}\n"
            f"📛 Nom : {channel_name}\n"
            f"👥 Abonnés : {subscribers}\n"
            f"📄 Description : {description.text}"
        )
        await bot.send_message(chat_id, details, reply_markup=empty_markup())

        # Notification dans le groupe de support
        send_group_message = (
            f"✅ <b>Nouveau canal soumis !</b>\n\n"
            f"🆔 ID : {channel_id}\n"
            f"📛 Nom : {channel_name}\n"
            f"👥 Abonnés : {subscribers}\n"
            f"📄 Description : {description.text}\n"
            f"🔑 Soumis par : @{admin_username}"
        )
        await bot.send_message(SUPPORT_GROUP, send_group_message)
        LOGGER.info(f"Canal ajouté : {channel_name}")

    except (ChannelPrivate, ChatAdminRequired) as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f"<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC",
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.message.chat.id, "❌ <b>Erreur : Le bot n'est pas administrateur ou le canal est privé.</b>", reply_markup=empty_markup())

    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(
            LOG_CHANNEL,
            f"<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC",
            parse_mode=enums.ParseMode.HTML
        )
        await bot.send_message(message.message.chat.id, "❌ <b>Une erreur inattendue s'est produite.</b>", reply_markup=empty_markup())
