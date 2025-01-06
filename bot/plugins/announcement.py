from pyrogram import filters,Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.user_db import get_admin,get_all,delete_user   
from bot.database.models.channel_db import total_channel                                                                                        
from bot.utils.markup import admin_markup,back_markup,empty_markup,announce_markup
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS,SUPPORT_GROUP,SUPPORT_CHANNEL

@Bot.on_callback_query(filters.regex('^announce$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def announcement_handler(bot:Client,message:Message):
    await bot.send_message(message.from_user.id, "✅ Choisissez la catégorie de l'annonce" ,reply_markup=announce_markup())
    
    
@Bot.on_callback_query(filters.regex('^close_reg$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def close_reg_handler(bot:Client,message:Message):
    data = f"""
🔰 L'inscription a été fermée

- La liste sera bientôt disponible.
- Restez à l'écoute !

<b>Total des canaux enregistrés :</b> {total_channel()}
"""


    await bot.send_message(SUPPORT_GROUP,data)
    LOGGER.info(f"Close Registration Message sent to @{SUPPORT_GROUP}")

    
@Bot.on_callback_query(filters.regex('^open_reg$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def open_reg_handler(bot:Client,message:Message):
    me=await bot.get_me()
    data = f"""
🔰 Inscription commencée 🔰

➖ Méthode de participation
1. <a href='https://t.me/{me.username}'>Cliquez ici pour participer</a>
2. Cliquez sur démarrer
3. Cliquez sur « Mes canaux » pour vérifier vos canaux enregistrés
4. Nouveaux membres, c'est une inscription unique. Vous n'avez pas besoin de réinscrire votre canal pour la prochaine promotion
5. Anciens membres, nous mettrons à jour le nombre d'abonnés des canaux via le bot. Ne vous inquiétez pas du nombre d'abonnés."

✅ Règles de la liste
- 2 heures au top
- 2 jours dans le canal
- 24 heures pour partager
————————————
⚠️ Type de promotion de liste
"""

    
    await bot.send_message(SUPPORT_GROUP,data)
    user_message = f""" 
ℹ️ Notification admin

✅ L'inscription a commencé

<b>Règles de la liste</b>
1. 2 heures 🔝 dans le canal
2. 2 jours dans le canal
3. 24 heures pour partager

<a href='https://t.me/{me.username}'>Cliquez ici pour participer</a>"""

    users=get_all()
    for user in users:
        try:
            await bot.send_message(user,user_message)
            LOGGER.info(f"Open Registration Message sent to {user}")
        except Exception as e:
            LOGGER.info(f"Open Registration message not sent to {user} ({e})")
            delete_user(user)
    await bot.send_message(message.message.chat.id, '☑️ Terminé !')
    LOGGER.info(f"Open Registration Message send to all")
    
@Bot.on_callback_query(filters.regex('^list_out$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def list_out_handler(bot:Client,message:Message):
    user_message = f"""
ℹ️ Notification admin

✅ La liste est sortie @{SUPPORT_CHANNEL}

Règles de la liste
1. 2 heures 🔝 dans le canal
2. 2 jours dans le canal
3. 24 heures pour partager"""

    users=get_all()
    for user in users:
        try:
            await bot.send_message(user,user_message)
            LOGGER.info(f"List out Message sent to {user}")
        except Exception as e:
            LOGGER.info(f"List out message not sent to {user} ({e})")
            delete_user(user)
    await bot.send_message(message.message.chat.id, '☑️ Terminé !')
    LOGGER.info(f"Message send to all")