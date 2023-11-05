

import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    MAINTENANCE_MODE = False  # Set this to True when maintenance mode is enabled
    
    # pyro client config
    API_ID    = os.environ.get("API_ID", "16743442")
    API_HASH  = os.environ.get("API_HASH", "12bbd720f4097ba7713c5e40a11dfd2a")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6410782788:AAGHH2trRETqKt1aGG_IFJ51htLvx0UgtiM") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","kakashi")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://jarvis:op@cluster0.7tisvwv.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://graph.org/file/e8b7439b7482e3ee0678e.mp4")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6299128233 6265459491').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002058050288"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))



class Txt(object):
    # part of text configuration
    START_TXT = """<b>Welcome {} 👋\nUnleash the magic of file renaming, thumbnail swapping, video-to-file conversion, custom captions, and more.\n• Crafted by <a href=https://t.me/BIackHatDev>Bʟᴀᴄᴋ Hᴀᴛ Dᴇᴠ</a> </b>"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 My name: <a href=http://t.me/KakashiHatake_xBot>Kᴀᴋᴀsʜɪ Hᴀᴛᴀᴋᴇ</a>
├🖥️ Developers: <a href=https://t.me/BIackHatDev>BʟᴀᴄᴋHᴀᴛDᴇᴠ</a> 
├📕 Library: <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
├✏️ Language: <a href=https://www.python.org>Pyᴛʜᴏɴ3</a>
├💾 Data Base: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
├📊 Build Version: `KH V4.7.0`
├🔗 GitHub: <a href=https://github.com/illuminati-Dev>GitHub</a>
├📧 Contact: <a href=https://telegram.com/>Soon</a>
╰───────────────⍟ """


    HELP_TXT = """
🌌 How To Set Thumbnail
  
• /start the bot and send any photo to automatically set the thumbnail.
• /del_thumb to delete your old thumbnail.
• /view_thumb to view your current thumbnail.

📑 How To Set Custom Caption
• /set_caption - Use this command to set a custom caption.
• /see_caption - Use this command to view your custom caption.
• /del_caption - Use this command to delete your custom caption.
Example: /set_caption 📕 File Name: {filename}
💾 Size: {filesize}
⏰ Duration: {duration}

👮 Admin Commands
• /addadmin (user_id) - Add a user as an admin.
• /rmadmin (user_id) - Remove admin status from a user.
• /ban (user_id) - Ban a user.
• /unban (user_id) - Unban a user.

✏️ How To Rename A File
• Send any file and type the new file name and select the format [document, video, audio].
"""


    DEV_TXT = """<b><u>🌟 Cᴏᴅᴇ ɪs ʟɪᴋᴇ ʜᴜᴍᴏʀ. Wʜᴇɴ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴇxᴘʟᴀɪɴ ɪᴛ, ɪᴛ’s ʙᴀᴅ.</u></b>\n
╭───────────⍟
├<b>👨‍💻 Dev : <a href="BIackHatDev.t.me">Bʟᴀᴄᴋ Hᴀᴛ Dᴇᴠ</a></b>
├<b>🔷 Brother: <a href="The_NanamiiKento.t.me">𝙽 𝙰 𝙽 𝙰 𝙼 𝙸</a></b>
├<b>🔷 Brother: <a href="NuMbEr03AnUrAg.t.me">©《@NUR∆G》™ 𝘽𝙀𝙉𝟏𝟎</a></b>
├<b>🔷 Brother: <a href="RomeoSama.t.me">Ꮢσᴍᴇᴏ 𝐒αᴍᴀ</a></b>
├<b>🔷 Brother: <a href="Shin_Shivaay.t.me">SASUKE 『सर्वेक्षण कोर</a></b>
├<b>🔷 Brother: <a href="Zoro_RTX.t.me">Zoro</a></b>
├<b>🔷 Brother: <a href="Theharxhu.t.me">Harxhu</a></b>
├<b>🔷 Brother: <a href="Trippy_xt.t.me">⚚ 𝐓𝐑𝐈𝐏𝐏𝐘 ❄️</a></b>
╰───────────────⍟
"""


    PROGRESS_BAR = """\n
╭━━━━❰Progress Bar❱━➣
┣⪼ 🗃️ Size: {1} | {2}
┣⪼ ⏳ Done : {0}%
┣⪼ 🚀 Speed: {3}/s
┣⪼ ⏰ Eᴛᴀ: {4}
┣⪼ 🌟 Keep Going! 
╰━━━━━━━━━━━━━━━➣ 
"""



