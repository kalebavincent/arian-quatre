async def is_bot_admin(bot,chat_id):
        admin=[]
        me=await bot.get_me()
        iters=await bot.get_chat_members(chat_id, filter="administrators")
        for member in iters :
            admin.append(member.user.username)
        print(admin)
        if me.username in admin:
            return True