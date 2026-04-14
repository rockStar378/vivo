import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.database import get_autoplay, get_cmode, set_autoplay
from VIVAANXMUSIC.utils.decorators.admins import AdminActual
from config import BANNED_USERS


# 🎨 Buttons UI
def autoplay_markup():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ ᴇɴᴀʙʟᴇ", callback_data="autoplay_on"),
                InlineKeyboardButton("⚡ ᴅɪꜱᴀʙʟᴇ", callback_data="autoplay_off"),
            ],
            [
                InlineKeyboardButton("🔄 ʀᴇꜰʀᴇꜱʜ", callback_data="autoplay_refresh"),
                InlineKeyboardButton("✖ ᴄʟᴏꜱᴇ", callback_data="autoplay_close"),
            ]
        ]
    )


# ⏳ Auto delete (non-blocking)
async def delete_later(msg):
    await asyncio.sleep(20)
    try:
        await msg.delete()
    except:
        pass


# 🎛 Command Handler
@app.on_message(filters.command(["autoplay", "cautoplay"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def autoplay_control(_, message: Message, strings):

    command = message.command[0].lower()

    # Channel mode
    if command.startswith("c"):
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text("❌ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ.")
        try:
            await app.get_chat(chat_id)
        except Exception:
            return await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ.")
    else:
        chat_id = message.chat.id

    status = "ᴇɴᴀʙʟᴇ" if await get_autoplay(chat_id) else "ᴅɪsᴀʙʟᴇ"
    chat_title = message.chat.title

    msg = await message.reply_text(
        f"❖ ᴀᴜᴛᴏ ᴘʟᴀʏ sᴇᴛᴛɪɴɢ ᴘᴀɴᴇʟ\n\n"
        f"🏵️ ɢʀᴏᴜᴘ ɪᴅ :- `{chat_id}`\n"
        f"🍂 sᴛᴀᴛᴜs :- {status} {'✅' if status == 'ᴇɴᴀʙʟᴇ' else '❌'}\n"
        f"🏖️ ɢʀᴏᴜᴘ ɴᴀᴍᴇ :- {chat_title}\n\n"
        f"❏ ᴛᴀᴘ ᴛᴏ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴄʜᴀɴɢᴇ ᴀᴜᴛᴏᴘʟᴀʏ sᴇᴛᴛɪɴɢ.",
        reply_markup=autoplay_markup()
    )

    asyncio.create_task(delete_later(msg))


# 🔘 Callback Buttons
@app.on_callback_query(filters.regex("^autoplay_"))
async def autoplay_buttons(client, callback_query):

    data = callback_query.data
    chat_id = callback_query.message.chat.id
    chat_title = callback_query.message.chat.title

    if data == "autoplay_on":
        await set_autoplay(chat_id, True)

    elif data == "autoplay_off":
        await set_autoplay(chat_id, False)

    elif data == "autoplay_refresh":
        pass

    elif data == "autoplay_close":
        return await callback_query.message.delete()

    else:
        return

    await callback_query.answer("ᴜᴘᴅᴀᴛᴇᴅ ✓")

    status = "ᴇɴᴀʙʟᴇ" if await get_autoplay(chat_id) else "ᴅɪsᴀʙʟᴇ"

    msg = await callback_query.message.edit_text(
        f"❖ ᴀᴜᴛᴏ ᴘʟᴀʏ sᴇᴛᴛɪɴɢ ᴘᴀɴᴇʟ\n\n"
        f"🏵️ ɢʀᴏᴜᴘ ɪᴅ :- `{chat_id}`\n"
        f"🍂 sᴛᴀᴛᴜs :- {status} {'✅' if status == 'ᴇɴᴀʙʟᴇ' else '❌'}\n"
        f"🏖️ ɢʀᴏᴜᴘ ɴᴀᴍᴇ :- {chat_title}\n\n"
        f"❏ ᴛᴀᴘ ᴛᴏ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴄʜᴀɴɢᴇ ᴀᴜᴛᴏᴘʟᴀʏ sᴇᴛᴛɪɴɢ.",
        reply_markup=autoplay_markup()
    )

    asyncio.create_task(delete_later(msg))