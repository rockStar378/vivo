from pyrogram.enums import ParseMode

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype, query: str = None, autoplay: bool = False):
    if await is_on_off(2):

        # Query handle
        if query is None:
            try:
                query = message.text.split(None, 1)[1]
            except Exception:
                query = "—"

        # Mode detect
        mode = "🔁 AUTOPLAY" if autoplay else "▶️ MANUAL"

        # Safe username handling
        chat_username = f"@{message.chat.username}" if message.chat.username else "None"
        user_username = f"@{message.from_user.username}" if message.from_user.username else "None"

        logger_text = f"""
<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴍᴏᴅᴇ :</b> {mode}

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {message.chat.title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {chat_username}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ɴᴀᴍᴇ :</b> {message.from_user.mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {user_username}

<b>ǫᴜᴇʀʏ :</b> {query}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}"""

        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
