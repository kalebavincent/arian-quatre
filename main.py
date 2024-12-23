import os

import random

import time
import string
import shutil
from flask import Flask
import psutil
import random
import asyncio
from PIL import Image
from configs import Config
# from pyromod import listen
from pyrogram import Client, filters, enums
from helpers.markup_maker import MakeButtons
from helpers.streamtape import UploadToStreamtape
from helpers.clean import delete_all
from hachoir.parser import createParser
from helpers.check_gap import CheckTimeGap
from helpers.database.access_db import db
from helpers.database.add_user import AddUserToDatabase
from helpers.uploader import UploadVideo
from helpers.settings import OpenSettings
from helpers.forcesub import ForceSub
from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
from helpers.broadcast import broadcast_handler
from helpers.ffmpeg import MergeVideo, generate_screen_shots, cult_small_video
from asyncio.exceptions import TimeoutError
from pyrogram.errors import FloodWait, UserNotParticipant, MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto

QueueDB = {}
ReplyDB = {}
FormtDB = {}
bot = Client(
    name=Config.SESSION_NAME,
    api_id=int(Config.API_ID),
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running. Made with ♥️ by Hyoshdesign"

def start_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@bot.on_message(filters.private & filters.command("start"))
async def start_handler(bot: Client, m: Message):
    await AddUserToDatabase(bot, m)
    Fsub = await ForceSub(bot, m)
    if Fsub == 400:
        return

    img_folder = Config.IMG_FOLDER
    img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if os.path.isfile(os.path.join(img_folder, f))]
    if img_files:
        random_img = random.choice(img_files)
    else:
        random_img = None  

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ℹ️ ɪɴꜰᴏ", url="https://t.me/hyoshcoder")],
            [
                InlineKeyboardButton("💬 ᴀᴅᴍɪɴꜱᴛʀᴀᴛᴇᴜʀ", url="https://t.me/hyoshdesign"),
                InlineKeyboardButton("📢 ᴄʜᴀîɴᴇ ᴅᴇꜱ ʙᴏᴛꜱ", url="https://t.me/hyoshmangavf"),
            ],
            [InlineKeyboardButton("⚙️ ᴏᴜᴠʀɪʀ ʟᴇꜱ ᴘᴀʀᴀᴍèᴛʀᴇꜱ", callback_data="openSettings")],
            [
              InlineKeyboardButton(" ᴀɪᴅᴇ", callback_data="help"),
              InlineKeyboardButton("ᴀ ᴘʀᴏᴘᴏꜱ", callback_data="about"),
            ],
            [InlineKeyboardButton("❌ ꜰᴇʀᴍᴇʀ", callback_data="closeMeh")],
        ]
    )

    if random_img:
        await m.reply_photo(
            photo=random_img,
            caption=Config.START_TEXT,
            reply_markup=reply_markup,
        )
    else:
        await m.reply_text(
            text=Config.START_TEXT,
            disable_web_page_preview=True,
            quote=True,
            reply_markup=reply_markup,
        )



@bot.on_message(filters.private & (filters.video | filters.document))
async def videos_handler(bot: Client, m: Message):
    if m.edit_date:
        return  
    await AddUserToDatabase(bot, m)
    Fsub = await ForceSub(bot, m)
    if Fsub == 400:
        return
    media = m.video or m.document
    if media.file_name is None:
        await m.reply_text("❌ ɴᴏᴍ ᴅᴜ ꜰɪᴄʜɪᴇʀ ɪɴᴛʀᴏᴜᴠᴀʙʟᴇ, ʀᴇɴᴏᴍᴍᴇʀ ʟᴇ ꜱᴜʀ ɴᴏᴛʀᴇ ʙᴏᴛ ꜰɪʟᴇ ʀᴇɴᴀᴍᴇʀ @HokageRenamer_bot ᴇxᴛᴇɴᴛɪᴏɴ ᴇꜱᴛ ʀᴇQᴜɪꜱ !")
        return
    if media.file_name.rsplit(".", 1)[-1].lower() not in ["mp4", "mkv", "webm"]:
        await m.reply_text("⚠️ ᴄᴇ ꜰᴏʀᴍᴀᴛ ᴅᴇ ᴠɪᴅéᴏ ɴ'ᴇꜱᴛ ᴘᴀꜱ ᴘʀɪꜱ ᴇɴ ᴄʜᴀʀɢᴇ !\nᴠᴇᴜɪʟʟᴇᴢ ᴇɴᴠᴏʏᴇʀ ᴜɴɪQᴜᴇᴍᴇɴᴛ ᴅᴇꜱ ꜰɪᴄʜɪᴇʀꜱ ᴍᴘ4, ᴍᴋᴠ ᴏᴜ ᴡᴇʙᴍ.", quote=True)
        return
    if QueueDB.get(m.from_user.id, None) is None:
        FormtDB.update({m.from_user.id: media.file_name.rsplit(".", 1)[-1].lower()})
    if (FormtDB.get(m.from_user.id, None) is not None) and (media.file_name.rsplit(".", 1)[-1].lower() != FormtDB.get(m.from_user.id)):
        await m.reply_text(f"⚠️ ᴠᴏᴜꜱ ᴀᴠᴇᴢ ᴅ'ᴀʙᴏʀᴅ ᴇɴᴠᴏʏé ᴜɴᴇ ᴠɪᴅéᴏ ᴅᴇ ᴛʏᴘᴇ **{FormtDB.get(m.from_user.id).upper()}**, veuillez maintenant envoyer uniquement ce type de vidéo.", quote=True)
        return
    input_ = f"{Config.DOWN_PATH}/{m.from_user.id}/input.txt"
    if os.path.exists(input_):
        await m.reply_text("🚫 ᴅéꜱᴏʟé,\nᴜɴᴇ ᴛâᴄʜᴇ ᴇꜱᴛ ᴅéᴊà ᴇɴ ᴄᴏᴜʀꜱ!\nᴍᴇʀᴄɪ ᴅᴇ ɴᴇ ᴘᴀꜱ ꜱᴘᴀᴍᴍᴇʀ.")
        return
    isInGap, sleepTime = await CheckTimeGap(m.from_user.id)
    if isInGap is True:
        await m.reply_text(f"🚫 ᴅéꜱᴏʟé,\nᴘᴀꜱ ᴅᴇ ꜰʟᴏᴏᴅ ᴀᴜᴛᴏʀɪꜱé!\nᴠᴇᴜɪʟʟᴇᴢ ᴇɴᴠᴏʏᴇʀ ᴜɴᴇ ᴠɪᴅéᴏ ᴀᴘʀèꜱ`{str(sleepTime)}s` !!", quote=True)
    else:
        editable = await m.reply_text("⏳ Veuillez patienter ...", quote=True)
        MessageText = "✅ ᴠɪᴅéᴏ ᴀᴊᴏᴜᴛéᴇ!\nᴇɴᴠᴏʏᴇᴢ ʟᴀ ᴠɪᴅéᴏ ꜱᴜɪᴠᴀɴᴛᴇ ᴏᴜ ᴀᴘᴘᴜʏᴇᴢ ꜱᴜʀ ʟᴇ ʙᴏᴜᴛᴏɴ **ꜰᴜꜱɪᴏɴɴᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴛ** !"
        if QueueDB.get(m.from_user.id, None) is None:
            QueueDB.update({m.from_user.id: []})
        if (len(QueueDB.get(m.from_user.id)) >= 0) and (len(QueueDB.get(m.from_user.id)) <= Config.MAX_VIDEOS):
            QueueDB.get(m.from_user.id).append(m.id) 
            if ReplyDB.get(m.from_user.id, None) is not None:
                await bot.delete_messages(chat_id=m.chat.id, message_ids=ReplyDB.get(m.from_user.id))
            if FormtDB.get(m.from_user.id, None) is None:
                FormtDB.update({m.from_user.id: media.file_name.rsplit(".", 1)[-1].lower()})
            await asyncio.sleep(Config.TIME_GAP)
            if len(QueueDB.get(m.from_user.id)) == Config.MAX_VIDEOS:
                MessageText = "✅ ᴛᴏᴜᴛ ᴇꜱᴛ ᴘʀêᴛ ! ᴀᴘᴘᴜʏᴇᴢ ᴍᴀɪɴᴛᴇɴᴀɴᴛ ꜱᴜʀ ʟᴇ ʙᴏᴜᴛᴏɴ **ꜰᴜꜱɪᴏɴɴᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴛ** !"
            markup = await MakeButtons(bot, m, QueueDB)
            await editable.edit(text="🎥 ᴠᴏᴛʀᴇ ᴠɪᴅéᴏ ᴀ éᴛé ᴀᴊᴏᴜᴛéᴇ à ʟᴀ ꜰɪʟᴇ ᴅ'ᴀᴛᴛᴇɴᴛᴇ !")
            reply_ = await m.reply_text(
                text=MessageText,
                reply_markup=InlineKeyboardMarkup(markup),
                quote=True
            )
            ReplyDB.update({m.from_user.id: reply_.id})
        elif len(QueueDB.get(m.from_user.id)) > Config.MAX_VIDEOS:
            markup = await MakeButtons(bot, m, QueueDB)
            await editable.edit(
                text=f"🚫 ᴅéꜱᴏʟé,\nᴜɴ ᴍᴀxɪᴍᴜᴍ ᴅᴇ {str(Config.MAX_VIDEOS)} ᴠɪᴅéᴏꜱ ᴘᴇᴜᴛ êᴛʀᴇ ꜰᴜꜱɪᴏɴɴé ᴇɴꜱᴇᴍʙʟᴇ  !\nᴀᴘᴘᴜʏᴇᴢ ᴍᴀɪɴᴛᴇɴᴀɴᴛ ꜱᴜʀ ʟᴇ ʙᴏᴜᴛᴏɴ **ꜰᴜꜱɪᴏɴɴᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴛ** !",
                reply_markup=InlineKeyboardMarkup(markup)
            )

@bot.on_message(filters.private & filters.photo)
async def photo_handler(bot: Client, m: Message):
    if m.edit_date:
        return  

    await AddUserToDatabase(bot, m)

    Fsub = await ForceSub(bot, m)

    if Fsub == 400:
        return

    editable = await m.reply_text("📥ꜱᴀᴜᴠᴇɢᴀʀᴅᴇ ᴅᴇ ʟᴀ ᴍɪɴɪᴀᴛᴜʀᴇ ᴅᴀɴꜱ ʟᴀ ʙᴀꜱᴇ ᴅᴇ ᴅᴏɴɴéᴇꜱ ...", quote=True)
    await db.set_thumbnail(m.from_user.id, thumbnail=m.photo.file_id)
    await editable.edit(
        text="✅ ᴍɪɴɪᴀᴛᴜʀᴇ ꜱᴀᴜᴠᴇɢᴀʀᴅéᴇ ᴀᴠᴇᴄ ꜱᴜᴄᴄèꜱ !",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("👁️ ᴠᴏɪʀ ʟᴀ ᴍɪɴɪᴀᴛᴜʀᴇ", callback_data="showThumbnail")],
                [InlineKeyboardButton("🗑️ ꜱᴜᴘᴘʀɪᴍᴇʀ ʟᴀ ᴍɪɴɪᴀᴛᴜʀᴇ", callback_data="deleteThumbnail")]
            ]
        )
    )


@bot.on_message(filters.private & filters.command("settings"))
async def settings_handler(bot: Client, m: Message):
    await AddUserToDatabase(bot, m)
    Fsub = await ForceSub(bot, m)
    if Fsub == 400:
        return
    
    editable = await m.reply_text("⚙️ ᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴅᴇꜱ ᴘᴀʀᴀᴍèᴛʀᴇꜱ, ᴠᴇᴜɪʟʟᴇᴢ ᴘᴀᴛɪᴇɴᴛᴇʀ ...", quote=True)
    await OpenSettings(editable, m.from_user.id)


@bot.on_message(filters.private & filters.command("broadcast") & filters.reply & filters.user(Config.BOT_OWNER))
async def _broadcast(_, m: Message):
    if m.edit_date:
        return  
    await broadcast_handler(m) 

@bot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def _status(_, m: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()

    await m.reply_text(
        text=(
            f"💾 **Espace disque total :** {total}\n"
            f"📂 **Espace utilisé :** {used} ({disk_usage}%)\n"
            f"📁 **Espace libre :** {free}\n"
            f"⚡ **Utilisation CPU :** {cpu_usage}%\n"
            f"🧠 **Utilisation RAM :** {ram_usage}%\n\n"
            f"👥 **Total des utilisateurs dans la base de données :** `{total_users}`"
        ),
        parse_mode=enums.ParseMode.MARKDOWN,
        quote=True
    )


@bot.on_message(filters.private & filters.command("check") & filters.user(Config.BOT_OWNER))
async def check_handler(bot: Client, m: Message):
    if len(m.command) == 2:
        editable = await m.reply_text(
            text="🔍 Vérification des détails de l'utilisateur ..."
        )
        try:
            user = await bot.get_users(user_ids=int(m.command[1]))
            detail_text = (
                f"**👤 Nom :** [{user.first_name}](tg://user?id={str(user.id)})\n"
                f"**🏷️ Nom d'utilisateur :** `{user.username}`\n"
                f"**📂 Upload en document :** `{await db.get_upload_as_doc(id=int(m.command[1]))}`\n"
                f"**🖼️ Générer des captures d'écran :** `{await db.get_generate_ss(id=int(m.command[1]))}`\n"
            )
            await editable.edit(
                text=detail_text,
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        except Exception as e:
            await editable.edit(
                text=f"❌ Une erreur est survenue : `{str(e)}`",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            
@bot.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    if "mergeNow" in cb.data:
        vid_list = list()
        await cb.message.edit(
            text="⏳ ᴠᴇᴜɪʟʟᴇᴢ ᴘᴀᴛɪᴇɴᴛᴇʀ ..."
        )
        duration = 0
        list_message_ids = QueueDB.get(cb.from_user.id, None)
        if list_message_ids is None:
            await cb.answer("🚫 ʟᴀ ꜰɪʟᴇ ᴅ'ᴀᴛᴛᴇɴᴛᴇ ᴇꜱᴛ ᴠɪᴅᴇ!", show_alert=True)
            await cb.message.delete(True)
            return
        list_message_ids.sort()
        input_ = f"{Config.DOWN_PATH}/{cb.from_user.id}/input.txt"
        if len(list_message_ids) < 2:
            await cb.answer("⚠️ ᴠᴏᴜꜱ ɴ'ᴀᴠᴇᴢ ᴇɴᴠᴏʏé Qᴜ'ᴜɴᴇ ꜱᴇᴜʟᴇ ᴠɪᴅéᴏ ᴘᴏᴜʀ ʟᴀ ꜰᴜꜱɪᴏɴ !", show_alert=True)
            await cb.message.delete(True)
            return
        if not os.path.exists(f"{Config.DOWN_PATH}/{cb.from_user.id}/"):
            os.makedirs(f"{Config.DOWN_PATH}/{cb.from_user.id}/")
        
        for i in (await bot.get_messages(chat_id=cb.from_user.id, message_ids=list_message_ids)):
            media = i.video or i.document
            if media is None:
                continue
            try:
                await cb.message.edit(
                    text=f"📥 ᴛéʟéᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴅᴇ : \n`{media.file_name}` ..."
                )
            except MessageNotModified:
                QueueDB.get(cb.from_user.id).remove(i.id)
                await cb.message.edit("⚡ ꜰɪᴄʜɪᴇʀ ɪɢɴᴏʀé !")
                await asyncio.sleep(3)
                continue

            file_dl_path = None
            try:
                c_time = time.time()
                file_dl_path = await bot.download_media(
                    message=i,
                    file_name=f"{Config.DOWN_PATH}/{cb.from_user.id}/{i.id}/",
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "📥 ᴛéʟéᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀꜱ ...",
                        cb.message,
                        c_time
                    )
                )
            except Exception as downloadErr:
                print(f"Éᴄʜᴇᴄ ᴅᴜ ᴛéʟéᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴅᴜ ꜰɪᴄʜɪᴇʀ !\nErreur : {downloadErr}")
                QueueDB.get(cb.from_user.id).remove(i.id)
                await cb.message.edit("⚡ ꜰɪᴄʜɪᴇʀ ɪɢɴᴏʀé !")
                await asyncio.sleep(3)
                continue

            metadata = extractMetadata(createParser(file_dl_path))
            try:
                if metadata.has("duration"):
                    duration += metadata.get('duration').seconds
                vid_list.append(f"file '{file_dl_path}'")
            except:
                await delete_all(root=f"{Config.DOWN_PATH}/{cb.from_user.id}/")
                QueueDB.update({cb.from_user.id: []})
                FormtDB.update({cb.from_user.id: None})
                await cb.message.edit("⚠️ ᴠɪᴅéᴏ ᴄᴏʀʀᴏᴍᴘᴜᴇ !\nᴠᴇᴜɪʟʟᴇᴢ ʀéᴇꜱꜱᴀʏᴇʀ ᴘʟᴜꜱ ᴛᴀʀᴅ.")
                return

        vid_list = list(set(vid_list))

        if len(vid_list) < 2:
            await cb.message.edit("⚠️ Une seule vidéo est dans la file d'attente !\nVous avez peut-être envoyé la même vidéo plusieurs fois.")
            return

        await cb.message.edit("🔄 Tentative de fusion des vidéos ...")
        with open(input_, 'w') as _list:
            _list.write("\n".join(vid_list))
        
        merged_vid_path = await MergeVideo(
            input_file=input_,
            user_id=cb.from_user.id,
            message=cb.message,
            format_=FormtDB.get(cb.from_user.id, "mkv")
        )

        if merged_vid_path is None:
            await cb.message.edit(
                text="⚠️ Échec de la fusion des vidéos !"
            )
            await delete_all(root=f"{Config.DOWN_PATH}/{cb.from_user.id}/")
            QueueDB.update({cb.from_user.id: []})
            FormtDB.update({cb.from_user.id: None})
            return
        await cb.message.edit("✅ Vidéo fusionnée avec succès !")
        await asyncio.sleep(Config.TIME_GAP)
        file_size = os.path.getsize(merged_vid_path)
        if int(file_size) > 2097152000:
            await cb.message.edit(f"📁 Désolé, la taille du fichier atteint {humanbytes(file_size)} !\nJe ne peux pas l'envoyer sur Telegram.\n\n📤 Envoi en cours vers Streamtape ...")
            await UploadToStreamtape(file=merged_vid_path, editable=cb.message, file_size=file_size)
            await delete_all(root=f"{Config.DOWN_PATH}/{cb.from_user.id}/")
            QueueDB.update({cb.from_user.id: []})
            FormtDB.update({cb.from_user.id: None})
            return
        await cb.message.edit(
            text="Souhaitez-vous renommer le fichier ?\nChoisissez une option ci-dessous :",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("✏️ Renommer le fichier", callback_data="renameFile_Yes")],
                    [InlineKeyboardButton("📂 Garder le nom par défaut", callback_data="renameFile_No")]
                ]
            )
        )
    elif "cancelProcess" in cb.data:
        await cb.message.edit("🔄 Suppression en cours du répertoire de travail ...")
        await delete_all(root=f"{Config.DOWN_PATH}/{cb.from_user.id}/")
        QueueDB.update({cb.from_user.id: []})
        FormtDB.update({cb.from_user.id: None})
        await cb.message.edit("❌ Annulation réussie !")
    elif cb.data.startswith("showFileName_"):
        message_ = await bot.get_messages(chat_id=cb.message.chat.id, message_ids=int(cb.data.split("_", 1)[-1]))
        try:
            await bot.send_message(
                chat_id=cb.message.chat.id,
                text="Voici le fichier demandé :",
                reply_to_message_id=message_.id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("❌ Supprimer le fichier", callback_data=f"removeFile_{str(message_.id)}")]
                    ]
                )
            )
        except FloodWait as e:
            await cb.answer("⛔ Merci d'éviter de spammer !", show_alert=True)
            await asyncio.sleep(e.x)
        except:
            media = message_.video or message_.document
            await cb.answer(f"Nom du fichier : {media.file_name}")
    elif "refreshFsub" in cb.data:
        if Config.UPDATES_CHANNEL:
            try:
                user = await bot.get_chat_member(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL), user_id=cb.message.chat.id)
                if user.status == "kicked":
                    await cb.message.edit(
                        text="🚫 Désolé, vous êtes banni de l'utilisation de ce bot. Contactez mon [Adminstrateur](https://t.me/botsupportastra).",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                try:
                    invite_link = await bot.create_chat_invite_link(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    invite_link = await bot.create_chat_invite_link(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
                await cb.message.edit(
                    text="**Rejoignez mon canal de mise à jour pour utiliser ce bot !**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Rejoindre le canal", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Rafraîchir", callback_data="refreshFsub")
                            ]
                        ]
                    ),
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                return
            except Exception:
                await cb.message.edit(
                    text="⚠️ Une erreur s'est produite. Contactez mon [Adminstrateur](https://t.me/botsupportastra).",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                return
        await cb.message.edit(
            text=Config.START_TEXT,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ℹ️ Infos", url="https://t.me/tweetface/2"), InlineKeyboardButton("Adminstrateur", url="https://t.me/botsupportastra")],
                [InlineKeyboardButton("Canal des Bots", url="https://t.me/hyoshdesign")]
            ]),
            disable_web_page_preview=True
        )
    elif "showThumbnail" in cb.data:
        db_thumbnail = await db.get_thumbnail(cb.from_user.id)
        if db_thumbnail is not None:
            await cb.answer("📤 Envoi de la miniature ...", show_alert=True)
            await bot.send_photo(
                chat_id=cb.message.chat.id,
                photo=db_thumbnail,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🗑️ Supprimer la miniature", callback_data="deleteThumbnail")]
                    ]
                )
            )
        else:
            await cb.answer("❌ Aucune miniature trouvée pour vous dans la base de données !")
    elif "deleteThumbnail" in cb.data:
        await db.set_thumbnail(cb.from_user.id, thumbnail=None)
        await cb.message.edit("🗑️ Miniature supprimée de la base de données !")
    elif "triggerUploadMode" in cb.data:
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc is False:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=True)
        elif upload_as_doc is True:
            await db.set_upload_as_doc(cb.from_user.id, upload_as_doc=False)
        await OpenSettings(m=cb.message, user_id=cb.from_user.id)
    elif "showQueueFiles" in cb.data:
        try:
            markup = await MakeButtons(bot, cb.message, QueueDB)
            await cb.message.edit(
                text="📋 Voici la liste des fichiers enregistrés dans votre file d'attente :",
                reply_markup=InlineKeyboardMarkup(markup)
            )
        except ValueError:
            await cb.answer("🛑 Votre file d'attente est vide !", show_alert=True)
    elif cb.data.startswith("removeFile_"):
        if (QueueDB.get(cb.from_user.id, None) is not None) or (QueueDB.get(cb.from_user.id) != []):
            QueueDB.get(cb.from_user.id).remove(int(cb.data.split("_", 1)[-1]))
            await cb.message.edit(
                text="🗑️ Fichier supprimé de la file d'attente !",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔙 Retour", callback_data="openSettings")]
                    ]
                )
            )
        else:
            await cb.answer("❌ Désolé, votre file d'attente est vide !", show_alert=True)
    elif "triggerGenSS" in cb.data:
        generate_ss = await db.get_generate_ss(cb.from_user.id)
        if generate_ss is True:
            await db.set_generate_ss(cb.from_user.id, generate_ss=False)
        elif generate_ss is False:
            await db.set_generate_ss(cb.from_user.id, generate_ss=True)
        await OpenSettings(cb.message, user_id=cb.from_user.id)
    elif "triggerGenSample" in cb.data:
        generate_sample_video = await db.get_generate_sample_video(cb.from_user.id)
        if generate_sample_video is True:
            await db.set_generate_sample_video(cb.from_user.id, generate_sample_video=False)
        elif generate_sample_video is False:
            await db.set_generate_sample_video(cb.from_user.id, generate_sample_video=True)
        await OpenSettings(cb.message, user_id=cb.from_user.id)
    elif "openSettings" in cb.data:
        await OpenSettings(cb.message, cb.from_user.id)
    elif cb.data.startswith("renameFile_"):
        if (QueueDB.get(cb.from_user.id, None) is None) or (QueueDB.get(cb.from_user.id) == []):
            await cb.answer("❌ Désolé, votre file d'attente est vide !", show_alert=True)
            return
        merged_vid_path = f"{Config.DOWN_PATH}/{str(cb.from_user.id)}/[@hyoshdesign]_Merged.{FormtDB.get(cb.from_user.id).lower()}"
        if cb.data.split("_", 1)[-1] == "Yes":
            await cb.message.edit("📝 D'accord,\nEnvoyez-moi le nouveau nom du fichier !")
            try:
                ask_: Message = await bot.listen(cb.message.chat.id, timeout=300)
                if ask_.text:
                    ascii_ = e = ''.join([i if (i in string.digits or i in string.ascii_letters or i == " ") else "" for i in ask_.text])
                    new_file_name = f"{Config.DOWN_PATH}/{str(cb.from_user.id)}/{ascii_.replace(' ', '_').rsplit('.', 1)[0]}.{FormtDB.get(cb.from_user.id).lower()}"
                    await cb.message.edit(f"✏️ Renommage du fichier en `{new_file_name.rsplit('/', 1)[-1]}`")
                    os.rename(merged_vid_path, new_file_name)
                    await asyncio.sleep(2)
                    merged_vid_path = new_file_name
            except TimeoutError:
                await cb.message.edit("⏳ Temps écoulé !\nLe fichier sera téléchargé avec le nom par défaut.")
                await asyncio.sleep(Config.TIME_GAP)
            except:
                pass
        await cb.message.edit("Extraction des données vidéo... 📊")
        duration = 1
        width = 100
        height = 100
        try:
            metadata = extractMetadata(createParser(merged_vid_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
        except:
            await delete_all(root=f"{Config.DOWN_PATH}/{cb.from_user.id}/")
            QueueDB.update({cb.from_user.id: []})
            FormtDB.update({cb.from_user.id: None})
            await cb.message.edit("La vidéo fusionnée est corrompue ! ❌\nRéessayez plus tard.")
            return
        video_thumbnail = None
        db_thumbnail = await db.get_thumbnail(cb.from_user.id)
        if db_thumbnail is not None:
            video_thumbnail = await bot.download_media(message=db_thumbnail, file_name=f"{Config.DOWN_PATH}/{str(cb.from_user.id)}/thumbnail/")
            Image.open(video_thumbnail).convert("RGB").save(video_thumbnail)
            img = Image.open(video_thumbnail)
            img.resize((width, height))
            img.save(video_thumbnail, "JPEG")
        else:
            video_thumbnail = Config.DOWN_PATH + "/" + str(cb.from_user.id) + "/" + str(time.time()) + ".jpg"
            ttl = random.randint(0, int(duration) - 1)
            file_generator_command = [
                "ffmpeg",
                "-ss",
                str(ttl),
                "-i",
                merged_vid_path,
                "-vframes",
                "1",
                video_thumbnail
            ]
            process = await asyncio.create_subprocess_exec(
                *file_generator_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            t_response = stdout.decode().strip()
            if video_thumbnail is None:
                video_thumbnail = None
            else:
                Image.open(video_thumbnail).convert("RGB").save(video_thumbnail)
                img = Image.open(video_thumbnail)
                img.resize((width, height))
                img.save(video_thumbnail, "JPEG")
        await UploadVideo(
            bot=bot,
            cb=cb,
            merged_vid_path=merged_vid_path,
            width=width,
            height=height,
            duration=duration,
            video_thumbnail=video_thumbnail,
            file_size=os.path.getsize(merged_vid_path)
        )
        caption = f"© @{(await bot.get_me()).username}"
        if (await db.get_generate_ss(cb.from_user.id)) is True:
            await cb.message.edit("Génération des captures d'écran en cours... 📸")
            generate_ss_dir = f"{Config.DOWN_PATH}/{str(cb.from_user.id)}"
            list_images = await generate_screen_shots(merged_vid_path, generate_ss_dir, 9, duration)
            if list_images is None:
                await cb.message.edit("Échec de la génération des captures d'écran ! ❌")
                await asyncio.sleep(Config.TIME_GAP)
            else:
                await cb.message.edit("Captures d'écran générées avec succès ! ✅\nTéléchargement en cours... ⬆️")
                photo_album = list()
                if list_images is not None:
                    i = 0
                    for image in list_images:
                        if os.path.exists(str(image)):
                            if i == 0:
                                photo_album.append(InputMediaPhoto(media=str(image), caption=caption))
                            else:
                                photo_album.append(InputMediaPhoto(media=str(image)))
                            i += 1
                await bot.send_media_group(
                    chat_id=cb.from_user.id,
                    media=photo_album
                )
        if ((await db.get_generate_sample_video(cb.from_user.id)) is True) and (duration >= 15):
            await cb.message.edit("Génération de la vidéo d'exemple en cours... 🎬")
            sample_vid_dir = f"{Config.DOWN_PATH}/{cb.from_user.id}/"
            ttl = int(duration*10 / 100)
            sample_video = await cult_small_video(
                video_file=merged_vid_path,
                output_directory=sample_vid_dir,
                start_time=ttl,
                end_time=(ttl + 10),
                format_=FormtDB.get(cb.from_user.id)
            )
            if sample_video is None:
                await cb.message.edit("Échec de la génération de la vidéo d'exemple ! ❌")
                await asyncio.sleep(Config.TIME_GAP)
            else:
                await cb.message.edit("Vidéo d'exemple générée avec succès ! ✅\nTéléchargement en cours... ⬆️")
                sam_vid_duration = 5
                sam_vid_width = 100
                sam_vid_height = 100
                try:
                    metadata = extractMetadata(createParser(sample_video))
                    if metadata.has("duration"):
                        sam_vid_duration = metadata.get('duration').seconds
                    if metadata.has("width"):
                        sam_vid_width = metadata.get("width")
                    if metadata.has("height"):
                        sam_vid_height = metadata.get("height")
                except:
                    await cb.message.edit("Fichier vidéo d'exemple corrompu ! ❌")
                    await asyncio.sleep(Config.TIME_GAP)
                try:
                    c_time = time.time()
                    await bot.send_video(
                        chat_id=cb.message.chat.id,
                        video=sample_video,
                        thumb=video_thumbnail,
                        width=sam_vid_width,
                        height=sam_vid_height,
                        duration=sam_vid_duration,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "Téléchargement de la vidéo d'exemple... ⬆️",
                            cb.message,
                            c_time,
                        )
                    )
                except Exception as sam_vid_err:
                    print(f"Erreur lors de la tentative de téléchargement de la vidéo d'exemple :\n{sam_vid_err}")
                    try:
                        await cb.message.edit("Échec du téléchargement de la vidéo d'exemple ! ❌")
                        await asyncio.sleep(Config.TIME_GAP)
                    except:
                        pass
        await cb.message.delete(True)
        await delete_all(root=f"{Config.DOWN_PATH}/{cb.from_user.id}/")
        QueueDB.update({cb.from_user.id: []})
        FormtDB.update({cb.from_user.id: None})
    elif "closeMeh" in cb.data:
        await cb.message.delete(True)
        await cb.message.reply_to_message.delete(True)


if __name__ == "__main__":
    from threading import Thread
    server_thread = Thread(target=start_server)
    server_thread.start()
    bot.run()


