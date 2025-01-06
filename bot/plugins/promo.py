from pyrogram import filters,Client, enums
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.user_db import get_admin,get_user_username
from bot.utils.markup import back_markup,empty_markup,promo_button_markup,send_promo_markup 
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS,SUPPORT_CHANNEL,SUPPORT_GROUP
from bot.database.models.post_db import get_buttons,get_post
from bot.database.models.channel_db  import get_channel,get_channel_by_id,chunck,Channel,session,get_user_channel_count
from bot.database.models.promo_db import save_message_ids,delete_promo,get_promo
from pyrogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired,ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden,ChatForbidden

a=list(chunck())
b=get_post()
p=f"🗣Via @{SUPPORT_CHANNEL} \n1 hr Top 24 hrs🔛 in Channel.\n━━━━━━━━━━━━━━━\n<a href='tg://user?id={SUDO_USERS}'>🔴PAID PROMOTION HERE🔴</a>\n━━━━━━━━━━━━━━━\n\n"
line='━━━━━━━━━━━━━━━'



@Bot.on_callback_query(filters.regex('^send_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_promo_handler(bot:Client,message:Message):
    await bot.send_message(message.message.chat.id,"✅ Choisissez la liste de promotion",reply_markup=send_promo_markup())
    
@Bot.on_callback_query(filters.regex('^delete_promotion$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def delete_promo_handler(bot:Client,message:Message):
    error_list=""
    promo=get_promo() 
    for i in promo:
            print(i.message_id)
            try:
                messages=await bot.delete_messages(i.channel,i.message_id)
                if messages is False:
                    x=get_channel_by_id(i.channel)
                    error_list+=f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
            except Exception as e:
                await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
                LOGGER.error(e)
    delete_promo()
    await bot.send_message(message.message.chat.id,"✅ TERMINÉ")
    await bot.send_message(message.from_user.id,f"Échec de la suppression de la liste de promotion\n\n {error_list}",disable_web_page_preview=True)
    
@Bot.on_callback_query(filters.regex('^send_classic_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_classic_promo_handler(bot:Client,message:Message):
    try:
            channl=''
            error_list=''
            li=1
            for i in a:
                val=""
                userdata=""
                for j in i:
                    ch=get_channel_by_id(j)
                    user=get_user_username(ch.chat_id)
                    channel_count=get_user_channel_count(ch.chat_id)
                    val+=f'{b.emoji}<a href="{ch.invite_link}">{str(ch.channel_name)}</a>\n'
                    dest=b.set_top+"\n\n"+val+"\n"+p+'\n'+b.set_bottom
                    userdata+=f'<code>@{user} ({channel_count})</code>\n'
                forward=await bot.send_message(SUPPORT_CHANNEL,dest,reply_markup=promo_button_markup(),disable_web_page_preview=True,parse_mode=enums.ParseMode.HTML)
                await bot.send_message(SUPPORT_CHANNEL,f"Admin Liste {li}\n\n{userdata}")
                li=li+1
                for x in i:
                    chname=get_channel_by_id(x)
                    try:
                        id_channel=await bot.forward_messages(chat_id=x,from_chat_id=SUPPORT_CHANNEL,message_ids=forward.message_id)
                        save_message_ids(x,id_channel.message_id)
                        channl+=f"✅ Nom du canal : {chname.channel_name}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.message_id)}\n{line}\n\n"
                        
                    except (ChatAdminRequired,ChannelPrivate,ChatWriteForbidden,ChatForbidden):
                        await bot.send_message(x.chat_id,f"Échec de l'envoi du message pour {x.channel_name}\nVeuillez republier la promotion pour éviter un bannissement")
                        error_list+=f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                    except Exception as e:
                        await bot.send_message(LOG_CHANNEL,f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
                        LOGGER.error(e)
                        
                await bot.send_message(SUPPORT_GROUP,f"#shared avec succès\n\n{channl} ",parse_mode=enums.ParseMode.MARKDOWN)
                await bot.send_message(SUPPORT_GROUP,f"#unsucessfull\n\n{error_list}")
                
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
            await bot.send_message(message.message.chat.id,"**⚠️ Un problème est survenu**",parse_mode=enums.ParseMode.MARKDOWN)


@Bot.on_callback_query(filters.regex('^send_standard_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_morden_promo_handler(bot:Client,message:Message):
    try:
            channl=''
            error_list=''
            li=1
            for i in a:
                val=""
                userdata=""
                for j in i:
                    ch=get_channel_by_id(j)
                    user=get_user_username(ch.chat_id)
                    channel_count=get_user_channel_count(ch.chat_id)
                    val+=f'\n\n<b>{str(ch.description)}</b>\n{b.emoji}<a href="{ch.invite_link}">「Rejoignez pour Utiliser le Bot」</a>{b.emoji}\n\n'
                    dest=b.set_top+"\n"+val+"\n"+p+b.set_bottom
                    userdata+=f'<code>@{user} ({channel_count})</code>\n'
                forward=await bot.send_message(SUPPORT_CHANNEL,dest,reply_markup=promo_button_markup(),disable_web_page_preview=True,parse_mode=enums.ParseMode.HTML)
                await bot.send_message(SUPPORT_CHANNEL,f"Admin Liste {li}\n\n{userdata}")
                li=li+1
                for x in i:
                    chname=get_channel_by_id(x)
                    try:
                        id_channel=await bot.forward_messages(chat_id=x,from_chat_id=SUPPORT_CHANNEL,message_ids=forward.message_id)
                        save_message_ids(x,id_channel.message_id)
                        channl+=f"✅ Nom du canal : {chname.channel_name}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.message_id)}\n{line}\n\n"
                        
                    except (ChatAdminRequired,ChannelPrivate,ChatWriteForbidden,ChatForbidden):
                        await bot.send_message(x.chat_id,f"Échec de l'envoi du message pour {x.channel_name}\nVeuillez republier la promotion pour éviter un bannissement")
                        error_list+=f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                    except Exception as e:
                        await bot.send_message(LOG_CHANNEL,f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
                        LOGGER.error(e)
                        
                await bot.send_message(SUPPORT_GROUP,f"#shared sucessfull\n\n{channl} ",parse_mode=enums.ParseMode.MARKDOWN)
                await bot.send_message(SUPPORT_GROUP,f"#unsucessfull\n\n{error_list}") 
                
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
            await bot.send_message(message.message.chat.id,"**⚠️ Un problème est survenu**",parse_mode=enums.ParseMode.MARKDOWN)
            
@Bot.on_callback_query(filters.regex('^send_desc_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_desc_promo_handler(bot:Client,message:Message):
    try:
            channl=''
            error_list=''
            li=1
            for i in a:
                val=""
                userdata=""
                for j in i:
                    ch=get_channel_by_id(j)
                    user=get_user_username(ch.chat_id)
                    channel_count=get_user_channel_count(ch.chat_id)
                    val+=f'\n<a href="{ch.invite_link}"><b>{str(ch.description)}</b></a>\n<b>––––––––––––––––––</b>\n\n'
                    dest=b.set_top+"\n"+val+"\n"+p+b.set_bottom
                    userdata+=f'<code> @{user} ({channel_count})</code>\n'
                forward=await bot.send_message(SUPPORT_CHANNEL,dest,reply_markup=promo_button_markup(),disable_web_page_preview=True,parse_mode=enums.ParseMode.HTML)
                await bot.send_message(SUPPORT_CHANNEL,f"Admin Liste {li}\n\n{userdata}")
                li=li+1
                for x in i:
                    chname=get_channel_by_id(x)
                    try:
                        id_channel=await bot.forward_messages(chat_id=x,from_chat_id=SUPPORT_CHANNEL,message_ids=forward.message_id)
                        save_message_ids(x,id_channel.message_id)
                        channl+=f"✅ Nom du canal : {chname.channel_name}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.message_id)}\n{line}\n\n"
                        
                    except (ChatAdminRequired,ChannelPrivate,ChatWriteForbidden,ChatForbidden):
                        await bot.send_message(x.chat_id,f"Échec de l'envoi du message pour {x.channel_name}\nVeuillez republier la promotion pour éviter un bannissement")
                        error_list+=f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                    except Exception as e:
                        await bot.send_message(LOG_CHANNEL,f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
                        LOGGER.error(e)
                        
                await bot.send_message(SUPPORT_GROUP,f"#shared sucessfull\n\n{channl} ",parse_mode=enums.ParseMode.MARKDOWN)
                await bot.send_message(SUPPORT_GROUP,f"#unsucessfull\n\n{error_list}") 
                
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
            await bot.send_message(message.message.chat.id,"**⚠️ Un problème est survenu**",parse_mode=enums.ParseMode.MARKDOWN)
            
            
@Bot.on_callback_query(filters.regex('^send_button_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def send_button_promo_handler(bot:Client,message:Message):
    try:
            channl=''
            error_list=''
            li=1
            buttons=[]
            down_buttons=get_buttons()
            bq=[InlineKeyboardButton(x.name,url=x.url) for x in down_buttons]
            buttons=[]
            for i in a:
                
                userdata=""
                
                for j in i:
                    ch=get_channel_by_id(j)
                    user=get_user_username(ch.chat_id)
                    channel_count=get_user_channel_count(ch.chat_id)
                    buttons.append(InlineKeyboardButton(ch.description,url=ch.invite_link))
                    
                    userdata+=f'<code> @{user} ({channel_count})</code>\n'
                markup=InlineKeyboardMarkup([buttons,bq])
                forward= await bot.send_photo(SUPPORT_CHANNEL,'bot/downloads/image.jpg',caption=b.set_caption,
                                    reply_markup=markup) 
                await bot.send_message(SUPPORT_CHANNEL,f"Admin Liste {li}\n\n{userdata}")
                li=li+1
                for x in i:
                    chname=get_channel_by_id(x)
                    try:
                        id_channel=await bot.forward_messages(chat_id=x,from_chat_id=SUPPORT_CHANNEL,message_ids=forward.message_id)
                        save_message_ids(x,id_channel.message_id)
                        channl+=f"✅ Nom du canal : {chname.channel_name}\nhttp://t.me/c/{str(x)[3:]}/{str(id_channel.message_id)}\n{line}\n\n"
                        
                    except (ChatAdminRequired,ChannelPrivate,ChatWriteForbidden,ChatForbidden):
                        await bot.send_message(x.chat_id,f"Échec de l'envoi du message pour {x.channel_name}\nVeuillez republier la promotion pour éviter un bannissement")
                        error_list+=f"🆔 ID : {x.channel_id}\n📛 Nom : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Lien : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
                    except Exception as e:
                        await bot.send_message(LOG_CHANNEL,f'<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
                        LOGGER.error(e)
                        
                await bot.send_message(SUPPORT_GROUP,f"#shared sucessfull\n\n{channl} ",parse_mode=enums.ParseMode.MARKDOWN)
                await bot.send_message(SUPPORT_GROUP,f"#unsucessfull\n\n{error_list}") 
                
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTemps : {time.ctime()} UTC',parse_mode=enums.ParseMode.HTML)
            await bot.send_message(message.message.chat.id,"**⚠️ Un problème est survenu**",parse_mode=enums.ParseMode.MARKDOWN)
