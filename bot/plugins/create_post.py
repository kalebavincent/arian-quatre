from pyrogram import filters,Client, enums
from pyrogram.types import CallbackQuery
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.user_db import get_admin                                                                                                    
from bot.utils.markup import admin_markup,back_markup,empty_markup,create_post_markup
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS
from bot.database.models.post_db import (add_button,
                                        delete_button,
                                        add_emoji,
                                        add_caption,
                                        add_bottom_text,
                                        add_top_text
                                         )
import re

@Bot.on_callback_query(filters.regex('^create_post$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def create_post_handler(bot:Client,message:Message):
    await bot.send_message(message.message.chat.id,"✅ Définir le champ requis",reply_markup=create_post_markup())
    
@Bot.on_callback_query(filters.regex('^set_button$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_button_handler(bot: Client, message: Message):
    # Demande du nom du bouton
    btn_name = await bot.ask(message.message.chat.id, "<b>✅ Envoyer le nom du bouton</b>", reply_markup=back_markup())
    
    if btn_name.text == '🚫 Cancel':
        await bot.send_message(message.message.chat.id, "Terminé", reply_markup=empty_markup())
    else:
        # Demande du lien du bouton
        btn_link = await bot.ask(message.message.chat.id, "<b>✅ Envoyer le lien du bouton</b>", reply_markup=back_markup())
        
        if btn_link.text == '🚫 Cancel':
            await bot.send_message(message.message.chat.id, "Terminé", reply_markup=empty_markup())
        else:
            # Vérification que le nom et l'URL sont valides
            if btn_name.text and btn_link.text:
                # Insertion dans la base de données
                add_button(btn_name.text, btn_link.text)
                await bot.send_message(
                    message.message.chat.id,
                    f"<b>✅ Bouton ajouté avec succès</b>\n\nNom : {btn_name.text}\nURL : {btn_link.text}",
                    reply_markup=empty_markup()
                )
            else:
                await bot.send_message(
                    message.message.chat.id,
                    "<b>❌ Nom ou URL du bouton manquant, veuillez réessayer</b>",
                    reply_markup=empty_markup()
                )
                
@Bot.on_callback_query(filters.regex('^delete_button$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def delete_button_handler(bot:Client,message:Message):
    delete_button()
    await bot.send_message(message.from_user.id,"Buttons supprimés avec succès")
    
    
@Bot.on_callback_query(filters.regex('^set_emoji$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_emoji_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer l'émoji**",parse_mode=enums.ParseMode.MARKDOWN,reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_emoji(msg.text)
        await bot.send_message(message.message.chat.id,f"Emoji definis avec succès défini {msg.text}",reply_markup=empty_markup())
        
@Bot.on_callback_query(filters.regex('^set_caption$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_caption_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer le texte avec le mode de formatage (si nécessaire)**",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_caption(msg.text)
        await bot.send_message(message.message.chat.id,f"Texte défini avec succès\n\n {msg.text}",
                                reply_markup=empty_markup(),
                                disable_web_page_preview=True) 
           
@Bot.on_callback_query(filters.regex('^set_top_text$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_top_text_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer le texte avec le mode de formatage (si nécessaire)**",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_top_text(msg.text)
        await bot.send_message(message.message.chat.id,f"Texte défini avec succès\n\n {msg.text}",
                                reply_markup=empty_markup(),
                                disable_web_page_preview=True)    

@Bot.on_callback_query(filters.regex('^set_bottom_text$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def set_bottom_text_handler(bot:Client,message:Message):
    msg=await bot.ask(message.message.chat.id,"**✅ Envoyer le texte avec le mode de formatage (si nécessaire)**",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=back_markup())
    
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminé",reply_markup=empty_markup())
    else:
        add_bottom_text(msg.text)
        await bot.send_message(message.message.chat.id,f"Texte défini avec succès\n\n {msg.text}",
                                reply_markup=empty_markup(),
                                disable_web_page_preview=True)  

@Bot.on_callback_query(filters.regex('^add_image$') & (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def add_image_handler(bot: Client, query: CallbackQuery):
    """Gestionnaire pour ajouter une image."""
    chat_id = query.message.chat.id
    
    # Demander à l'utilisateur d'envoyer une image
    await query.message.reply_text(
        "**✅ Envoyez une image :**",
        parse_mode=enums.ParseMode.MARKDOWN,
        reply_markup=back_markup()
    )
    
    try:
        # Attente de la réponse de l'utilisateur
        msg: Message = await bot.listen(chat_id, timeout=60)  # Timeout après 60 secondes
        
        # Vérifier si l'utilisateur annule
        if msg.text == '🚫 Annuler':
            await bot.send_message(
                chat_id,
                "❌ Action annulée.",
                reply_markup=empty_markup()
            )
            return
        
        # Vérifier si un média est envoyé
        if msg.photo or msg.document:
            file_name = "image.jpg" if msg.photo else msg.document.file_name
            
            # Télécharger l'image
            await bot.download_media(
                message=msg,
                file_name=file_name,
                progress=progress
            )
            
            await bot.send_message(
                chat_id,
                f"✅ Image enregistrée avec succès sous le nom `{file_name}`.",
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=empty_markup()
            )
        else:
            # Aucun média valide reçu
            await bot.send_message(
                chat_id,
                "❌ Action invalide. Veuillez envoyer une image ou un fichier valide.",
                reply_markup=empty_markup()
            )
    except TimeoutError:
        # Gérer les réponses tardives ou absentes
        await bot.send_message(
            chat_id,
            "⏳ Temps écoulé. Veuillez réessayer.",
            reply_markup=empty_markup()
        )
    except Exception as e:
        LOGGER.error(f"Erreur dans `add_image_handler` : {e}")
        await bot.send_message(
            chat_id,
            "❌ Une erreur s'est produite. Veuillez réessayer.",
            reply_markup=empty_markup()
        )


def progress(current, total):
    """Affiche la progression du téléchargement."""
    LOGGER.info(f"Téléchargement : {current * 100 / total:.1f}%")
    
