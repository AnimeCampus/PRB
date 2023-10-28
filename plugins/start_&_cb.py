
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from helper.database import db
from config import Config, Txt  



# Command to add an admin
@Client.on_message(filters.command("addadmin") & filters.user(Config.ADMIN))
async def add_admin(client, message):
    # Check if a user ID is provided in the command
    if len(message.command) > 1:
        user_id = int(message.command[1])
        await db.add_admin(user_id)
        await message.reply_text(f"User {user_id} has been added as an admin.")
    else:
        await message.reply_text("Please provide the user's ID to add them as an admin.")

# Command to remove an admin
@Client.on_message(filters.command("rmadmin") & filters.user(Config.ADMIN))
async def remove_admin(client, message):
    # Check if a user ID is provided in the command
    if len(message.command) > 1:
        user_id = int(message.command[1])
        await db.remove_admin(user_id)
        await message.reply_text(f"User {user_id} has been removed as an admin.")
    else:
        await message.reply_text("Please provide the user's ID to remove them as an admin.")

  
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user is banned
    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        # Send a message indicating that the user is banned
        await message.reply("You are banned by the admin.")
    else:
        # User is not banned, continue with the regular start message
        await db.add_user(client, message)
        button = InlineKeyboardMarkup([[            
            InlineKeyboardButton("👨‍💻 Devs 👨‍💻", callback_data='dev')
                ],[
                InlineKeyboardButton('🎛 About', callback_data='about'),
                InlineKeyboardButton('🛠 Help', callback_data='help')
                ],[               
                InlineKeyboardButton('📯 Updates', url='https://t.me/Emperors_Network')            
        ]])
        
        # Assuming you have a video file named 'start_video.mp4' in the same directory as your script
        START_VID = 'https://graph.org/file/e8b7439b7482e3ee0678e.mp4'
        
        await message.reply_video(START_VID, caption=Txt.START_TXT.format(user.mention), reply_markup=button)


# Add these import statements at the top of your code
from pyrogram.types import Message

@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.ADMIN))
async def rban_user(client, message):
    if len(message.command) != 2:
        await message.reply("Usage: /ban (user_id)")
        return

    user_id = int(message.command[1])

    # Ban the user in the database
    await db.ban_user(user_id)

    await message.reply(f"User with ID {user_id} is banned.")

@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.ADMIN))
async def runban_user(client, message):
    if len(message.command) != 2:
        await message.reply("Usage: /unban (user_id)")
        return

    user_id = int(message.command[1])

    # Unban the user in the database
    await db.unban_user(user_id)

    await message.reply(f"User with ID {user_id} is unbanned.")
              

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("👨‍💻 Devs 👨‍💻", callback_data='dev')
                ],[
                InlineKeyboardButton('🎛 About', callback_data='about'),
                InlineKeyboardButton('🛠 Help', callback_data='help')
                ],[               
                InlineKeyboardButton('📯 Updates', url='https://t.me/Emperors_Network')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔒 Close", callback_data = "close"),
                InlineKeyboardButton("◀️ Back", callback_data = "start")
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔒 Close", callback_data = "close"),
                InlineKeyboardButton("◀️ Back", callback_data = "start")
            ]])            
        )
    elif data == "dev":
        await query.message.edit_text(
            text=Txt.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔒 Close", callback_data = "close"),
                InlineKeyboardButton("◀️ Back", callback_data = "start")
            ]])          
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()


@Client.on_message(filters.private & filters.command("profile"))
async def user_profile(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user has set a name and photo
    user_name = await db.get_name(user_id)
    user_photo = await db.get_photo(user_id)

    if user_name and user_photo:
        caption = f"Name: {user_name}\n"
        await message.reply_photo(photo=user_photo, caption=caption)
    else:
        await message.reply_text("You don't have a profile set. Create a new profile using /cprofile.")
        
# Define a dictionary to track ongoing profile creation
temp_profile_creation = {}

@Client.on_message(filters.private & filters.command("cprofile"))
async def create_profile(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user already has a name and photo
    user_name = await db.get_name(user_id)
    user_photo = await db.get_photo(user_id)

    if user_name and user_photo:
        await message.reply_text("You already have a profile set.")
    else:
        await message.reply_text("Let's create a new profile. Send your name.")

        # Store the user ID to track the ongoing profile creation
        temp_profile_creation[user_id] = {"name": None, "photo": None}

@Client.on_message(filters.private & filters.text)
async def receive_name(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user is in the process of creating a profile
    if user_id in temp_profile_creation:
        user_name = message.text

        # Set the user's name in the temporary data structure
        temp_profile_creation[user_id]["name"] = user_name

        # Ask the user to send their profile photo
        await message.reply_text("Great! Now, send your profile photo.")

@Client.on_message(filters.private & filters.photo)
async def receive_photo(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user is in the process of creating a profile
    if user_id in temp_profile_creation:
        user_photo = message.photo.file_id

        # Set the user's photo in the temporary data structure
        temp_profile_creation[user_id]["photo"] = user_photo

        # Display the user's newly created profile
        caption = f"Name: {temp_profile_creation[user_id]['name']}"
        await message.reply_photo(photo=user_photo, caption=caption)

        # Clear the temporary profile creation data
        del temp_profile_creation[user_id]

        # Clear the temporary profile creation data
        del temp_profile_creation[user_id]
