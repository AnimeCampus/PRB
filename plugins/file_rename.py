import re
import os
import time
import asyncio
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from config import Config  # Replace with your configuration
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

# Function to extract 'episode' and 'quality' from user input
def extract_episode_quality(input_text):
    episode = re.search(r'(\d+)-episode', input_text, re.IGNORECASE)
    quality = re.search(r'\[([^\]]+)\]', input_text)

    episode_value = episode.group(1) if episode else "01"
    quality_value = quality.group(1) if quality else "HD"

    return episode_value, quality_value

# Function to rename media files
async def rename_media_file(client, message, episode, quality):
    file = getattr(message, message.media.value)
    media = getattr(file, file.media.value)

    new_filename = f"{file.file_name} {episode}-{quality}"
    extn = file.file_name.rsplit('.', 1)[-1] if "." in file.file_name else "mkv"
    new_name = new_filename + "." + extn

    # Rename the media file
    # You can implement the file renaming logic here
    # This is just a placeholder
    renamed_file_path = f"downloads/{new_name}"

    # Move or rename the file to the new path
    os.rename(file.file_path, renamed_file_path)

    # Now you have the renamed file in 'renamed_file_path'
    # You can process and upload it as needed

# Bot command to initiate auto-renaming
@app.on_message(filters.command("Autorename", prefixes="/"))
async def auto_rename_files(client, message):
    user = message.from_user
    user_id = user.id

    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        await message.reply_text("You are banned by the admin.")
    else:
        while not await db.is_user_admin(user_id):
            await message.reply_text("You are not authorized to use this feature. To gain authorization, please message owner @BIackHatDev")
            await asyncio.sleep(60)
            user = await client.get_users(user_id)
            user_id = user.id

        # Extract 'episode' and 'quality' from the command arguments
        command_parts = message.text.split(" ")
        if len(command_parts) < 3:
            await message.reply("Invalid command format. Please use: /Autorename episode quality")
            return

        episode = command_parts[1]
        quality = command_parts[2]

        # Rename the media file
        await rename_media_file(client, message, episode, quality)

# Callback to handle document upload
@app.on_callback_query(filters.regex("upload_document"))
async def doc(bot, update):
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message

    ms = await update.message.edit("Trying to download....")
    try:
        path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download started....", ms, time.time()))
    except Exception as e:
        return await ms.edit(e)

    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if "duration" in metadata:
            duration = metadata.get("duration").seconds
    except:
        pass

    ph_path = None
    user_id = int(update.message.chat.id)
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Your caption error except keyword Arguments●> ({e}")
    else:
        caption = f"**{new_filename}"

    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    await ms.edit("Trying to upload....")
    type = update.data.split("_")[1]
    try:
        if type == "document":
            await bot.send_document(
                update.message.chat.id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time()))
        elif type == "video":
            await bot.send_video(
                update.message.chat.id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time()))
        elif type == "audio":
            await bot.send_audio(
                update.message.chat.id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Upload Started....", ms, time.time()))
    except Exception as e:
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        await ms.edit(f" Error {e}")

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)

# Your other code (e.g., main function and setup) can remain the same
