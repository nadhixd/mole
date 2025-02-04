from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from ...modules.helpers.wrapper import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues

# Ensure you have the right imports for your context
# Assuming call is defined in SHUKLA.modules.utilities.calls
from SHUKLA.modules.utilities.calls import call

@app.on_message(cdx(["skp", "skip"]) & ~filters.private)
@sudo_users_only
async def skip_stream(client, message):
    chat_id = message.chat.id
    print(f"Debug: chat_id = {chat_id}")  # Debugging line to check chat_id
    
    # Fetch the call for the current chat
    calls = await call.calls
    chat_call = calls.get(chat_id)
    
    try:
        if chat_call:
            status = chat_call.status
            if (
                status == Call.Status.PLAYING
                or status == Call.Status.PAUSED
            ):
                queues.task_done(chat_id)
                if queues.is_empty(chat_id):
                    await call.leave_call(chat_id)
                    return await eor(message, "**Empty Queue, So\nLeaving VC!**")
                check = queues.get(chat_id)
                file = check["file"]
                type = check["type"]
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                return await eor(message, "**Stream Skipped!**")
            elif status == Call.Status.IDLE:
                await eor(message, "**Nothing Playing!**")
        else:
            await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Error: {e}")
        await eor(message, f"**Error occurred: {e}**")

@app.on_message(cdz(["cskp", "cskip"]) & ~filters.private)
@sudo_users_only
async def skip_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    
    print(f"Debug: chat_id fetched from get_chat_id = {chat_id}")  # Debugging line to check chat_id
    
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    
    calls = await call.calls
    chat_call = calls.get(chat_id)
    
    try:
        if chat_call:
            status = chat_call.status
            if (
                status == Call.Status.PLAYING
                or status == Call.Status.PAUSED
            ):
                queues.task_done(chat_id)
                if queues.is_empty(chat_id):
                    await call.leave_call(chat_id)
                    return await eor(message, "**Empty Queue, So\nLeaving VC!**")
                check = queues.get(chat_id)
                file = check["file"]
                type = check["type"]
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                return await eor(message, "**Stream Skipped!**")
            elif status == Call.Status.IDLE:
                await eor(message, "**Nothing Playing!**")
        else:
            await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Error: {e}")
        await eor(message, f"**Error occurred: {e}**")

async def get_chat_id(user_id):
    # Replace with your logic to fetch the chat_id for the user
    # If there's no chat associated, return 0 or None
    chat_id = 0  # Default value
    # Your logic to fetch the chat_id
    return chat_id