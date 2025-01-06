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
    channel = await bot.ask(message.message.chat.id, "✅ <b>Faites de ce bot un administrateur et transférez le message depuis le canal</b>", reply_markup=back_markup())
    if channel.text == '🚫 Cancel':
        await bot.send_message(message.message.chat.id, "🚫 <b>Annulé</b>", reply_markup=empty_markup())
    else:
        try:
            chat_id = message.from_user.id
            channel_id = channel.forward_from_chat.id
            channel_name = channel.forward_from_chat.title
            if is_channel_ban(channel_id):
                await bot.send_message(channel.from_user.id, "Aww :( , Ce canal est banni.")
                return

            if is_channel_exist(channel_id):
                await bot.send_message(channel.from_user.id, "Aww :( , Le canal existe déjà.")
                return

            if await is_bot_admin(bot, channel.forward_from_chat.id) is True:
                limit = get_subcribers_limit()
                subscribers = await bot.get_chat_members_count(channel_id)
                if subscribers >= limit:
                    description = await bot.ask(message.from_user.id, "<b>✅ Envoyez la description (maximum 5 mots et 2 emojis)</b>")
                    admin_username = message.from_user.username
                    invite_link = await bot.export_chat_invite_link(channel_id)
                    channel_data(chat_id, channel_id, channel_name, subscribers, admin_username, description.text, invite_link)
                    details = f'✅ <b>Canal soumis avec succès</b>\n\nID du canal : {channel_id}\nNom du canal : {channel_name}\nAbonnés : {subscribers}\nDescription : {description.text}'         
                    await bot.send_message(message.message.chat.id, details, reply_markup=empty_markup())
                    send_group_message = f'✅ <b>Un nouveau canal soumis !</b>\n\nID du canal : {channel_id}\nNom du canal : {channel_name}\nAbonnés : {subscribers}\nDescription : {description.text}\nSoumis par : @{admin_username}'
                    await bot.send_message(SUPPORT_GROUP, send_group_message)
                    LOGGER.info(f"Canal ajouté {channel_name}")
                else:
                    await bot.send_message(message.from_user.id, f"Vous avez besoin d'au moins {limit} abonnés pour vous inscrire", reply_markup=empty_markup())
            else:
                await bot.send_message(channel.chat.id, "<b> ❌ Le bot n'est pas administrateur</b>", reply_markup=empty_markup())
        
        except (ChannelPrivate, ChatAdminRequired) as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
            await bot.send_message(message.message.chat.id, "<b>❌ Le bot n'est pas administrateur</b>", reply_markup=empty_markup())
                

        except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL, f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC', parse_mode=enums.ParseMode.HTML)
            await bot.send_message(message.message.chat.id, "<b>❌ Action invalide</b>", reply_markup=empty_markup())
