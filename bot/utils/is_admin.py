from pyrogram.enums import ChatMembersFilter 

async def is_bot_admin(bot, chat_id):
    admins = []
    me = await bot.get_me()

    async for member in bot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        admins.append(member.user.username)
    print(admins)  
    return me.username in admins
