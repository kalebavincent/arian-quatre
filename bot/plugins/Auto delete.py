from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatType
from datetime import timedelta
import asyncio

# Stocke les configurations de suppression automatique : {chat_id: {"delay": timedelta, "enabled": True}}
auto_delete_settings = {}

def parse_delay_string(delay_str: str):
    """Convertit une chaîne comme '30m', '2h', '1d' en timedelta."""
    try:
        if delay_str.endswith("m"):  # Minutes
            return timedelta(minutes=int(delay_str[:-1]))
        elif delay_str.endswith("h"):  # Heures
            return timedelta(hours=int(delay_str[:-1]))
        elif delay_str.endswith("d"):  # Jours
            return timedelta(days=int(delay_str[:-1]))
        else:
            return None
    except ValueError:
        return None

@Client.on_message(filters.regex(r"^/setdelay\s*(\d+[mhd]|off)$") & filters.chat)
async def set_delay(client: Client, message: Message):
    """Commande pour définir ou désactiver la suppression automatique."""
    chat_id = message.chat.id

    # Vérifier si le message vient d'un groupe, supergroupe ou canal
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
        await message.reply(
            "Cette commande peut seulement être utilisée dans un groupe, supergroupe ou canal.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    command = message.text.split(maxsplit=1)

    if len(command) < 2:
        await message.reply(
            "Utilisation : `/setdelay 30m` ou `/setdelay off`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    delay_str = command[1].lower()

    if delay_str == "off":
        auto_delete_settings.pop(chat_id, None)
        await message.reply(
            "La suppression automatique des messages a été désactivée pour ce chat.",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        delay = parse_delay_string(delay_str)
        if delay:
            auto_delete_settings[chat_id] = {"delay": delay, "enabled": True}
            await message.reply(
                f"La suppression automatique est activée avec un délai de `{delay_str}`.",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await message.reply(
                "Format de délai invalide. Utilisez `Xm`, `Xh`, ou `Xd`.",
                parse_mode=ParseMode.MARKDOWN,
            )

@Client.on_message(filters.chat)
async def auto_delete(client: Client, message: Message):
    """Surveille les messages dans les chats où la suppression automatique est activée."""
    chat_id = message.chat.id

    # Vérifie si la suppression automatique est activée pour ce chat
    if chat_id in auto_delete_settings and auto_delete_settings[chat_id]["enabled"]:
        delay = auto_delete_settings[chat_id]["delay"]
        await asyncio.sleep(delay.total_seconds())
        try:
            await client.delete_messages(chat_id, message.message_id)
        except Exception as e:
            print(f"Erreur lors de la suppression d'un message dans {chat_id} : {e}")
