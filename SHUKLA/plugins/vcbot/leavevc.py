from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound

from ... import app, eor, cdx, cdz
from ...modules.mongo.streams import *
from ...modules.utilities import queues
from ...modules.utilities.calls import call  # ✅ Ensure 'call' is correctly imported
from ...modules.helpers.wrapper import sudo_users_only  # ✅ Ensure sudo_users_only is imported
from ...modules.mongo.chats import get_chat_id  # ✅ Ensure get_chat_id is imported

@app.on_message(cdx(["lve", "leave", "leavevc"]) & ~filters.private)
@sudo_users_only
async def leave_vc(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)  # ✅ Ensure 'call' is correctly used
        if a and a.status in ["not_playing", "playing", "paused"]:
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**Left VC!**")
        else:
            await eor(message, "**Nothing is Playing!**")
    except GroupCallNotFound:
        await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Error: {e}")

@app.on_message(cdz(["clve", "cleave", "cleavevc"]))
@sudo_users_only
async def leave_vc_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    
    if not chat_id:
        return await eor(message, "**🥀 No Stream Chat Set❗**")

    try:
        a = await call.get_call(chat_id)
        if a and a.status in ["not_playing", "playing", "paused"]:
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**Left VC!**")
        else:
            await eor(message, "**Nothing is Playing!**")
    except GroupCallNotFound:
        await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Error: {e}")