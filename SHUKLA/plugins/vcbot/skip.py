from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.types import Call
from pytgcalls import PyTgCalls

# Import necessary modules and functions
from ... import app, eor, cdx, cdz
from ...modules.helpers.wrapper import sudo_users_only
from ...modules.mongo.streams import get_chat_id
from ...modules.utilities import queues
from ...modules.utilities.streams import run_stream
from SHUKLA.modules.utilities.calls import call

@app.on_message(cdx(["skp", "skip"]) & ~filters.private)
@sudo_users_only
async def skip_stream(client, message):
    chat_id = message.chat.id

    try:
        calls = await call.calls  # Ensure call is correctly defined
        chat_call = calls.get(chat_id)

        if chat_call:
            status = chat_call.status
            if status in [Call.Status.PLAYING, Call.Status.PAUSED]:
                queues.task_done(chat_id)
                if queues.is_empty(chat_id):
                    await call.leave_call(chat_id)
                    return await eor(message, "**Queue is empty, leaving VC!**")

                check = queues.get(chat_id)
                file = check["file"]
                type = check["type"]
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                return await eor(message, "**Stream Skipped!**")
            
            elif status == Call.Status.IDLE:
                return await eor(message, "**Nothing is playing!**")

        return await eor(message, "**I am not in VC!**")

    except Exception as e:
        return await eor(message, f"**Error: {e}**")


@app.on_message(cdz(["cskp", "cskip"]) & ~filters.private)
@sudo_users_only
async def skip_stream_(client, message):
    user_id = message.from_user.id

    try:
        chat_id = await get_chat_id(user_id)  # Ensure get_chat_id is correctly defined
        if chat_id == 0:
            return await eor(message, "**🥀 No Stream Chat Set❗**")

        calls = await call.calls
        chat_call = calls.get(chat_id)

        if chat_call:
            status = chat_call.status
            if status in [Call.Status.PLAYING, Call.Status.PAUSED]:
                queues.task_done(chat_id)
                if queues.is_empty(chat_id):
                    await call.leave_call(chat_id)
                    return await eor(message, "**Queue is empty, leaving VC!**")

                check = queues.get(chat_id)
                file = check["file"]
                type = check["type"]
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                return await eor(message, "**Stream Skipped!**")
            
            elif status == Call.Status.IDLE:
                return await eor(message, "**Nothing is playing!**")

        return await eor(message, "**I am not in VC!**")

    except Exception as e:
        return await eor(message, f"**Error: {e}**")