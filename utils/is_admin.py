from pyrogram.enums import ChatMembersFilter

async def is_bot_admin(bot, chat_id):
    # Obtenir les informations du bot
    me = await bot.get_me()
    
    # Vérifier parmi les administrateurs
    async for member in bot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == me.id:  # Comparer par ID, plus fiable
            return True
    return False
