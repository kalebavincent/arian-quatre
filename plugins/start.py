import asyncio
from pyrogram import Client, filters, enums
from helper.ms_gen import ReactionMessage

last_sent_messages = {}
@Client.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    m = await message.reply_text("Démarrage en cours...")
    await asyncio.sleep(0.9)
    await m.delete()
    
    me = await client.get_me()
    bot_username = me.username
    bot_mention = me.mention
    username = message.from_user.username or "Cher utilisateur"

    await message.reply_text(
        f"👋 **Bienvenue, {username} !**\n\n"
        f"Je suis **[{bot_username}](tg://user?id={me.id})**, votre assistant personnel 🤖.\n\n"
        f"✨ Mon rôle principal est de **publier des phrases motivantes** à la fin de vos messages dans les groupes ou canaux que vous gérez. "
        f"C'est une excellente façon de maintenir une ambiance positive et engageante dans vos communautés !\n\n"
        f"🔧 **Configuration rapide** :\n"
        f"1️⃣ **Ajoutez-moi à vos groupes ou canaux.**\n"
        f"2️⃣ **Donnez-moi les permissions nécessaires pour publier et supprimer des messages.**\n\n"
        f"🚀 Une fois ces étapes terminées, je m'occuperai du reste !\n\n"
        f"Si vous avez besoin d'aide ou souhaitez en savoir plus, n'hésitez pas à me contacter ici ou via [**@{bot_username}**](tg://user?id={me.id}).\n\n"
        f"🎉 **Ajoute moi et laisse moi te surprendre !**",
        parse_mode=enums.ParseMode.MARKDOWN
    )



@Client.on_message(filters.channel | filters.group)
async def on_new_post(client, message):
    chat_id = message.chat.id
    me = await client.get_me()
    bot_username = me.username
    
    permissions = 1
    if permissions == 1:
        if chat_id in last_sent_messages:
            last_message_id = last_sent_messages[chat_id]
            try:
                await client.delete_messages(chat_id, last_message_id)
            except Exception:
                pass

        ms = ReactionMessage()
        message_text = ms.get_random_message()
        try:
            new_message = await client.send_message(
                chat_id, 
                f"||**{message_text}** \n @{bot_username}||",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            last_sent_messages[chat_id] = new_message.id
        except Exception:
            pass
