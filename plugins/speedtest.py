import os
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("speedtest"))
async def run_speedtest(client: Client, message: Message):
    m = await message.reply_text("⚡️ Running Speedtest")

    try:
        # Run the fast-cli command to check internet speed
        speedtest_result = os.popen("fast").read()

        # Extract download and upload speeds from the result
        download_speed = None
        upload_speed = None

        for line in speedtest_result.split('\n'):
            if "Download" in line:
                download_speed = line.strip()
            elif "Upload" in line:
                upload_speed = line.strip()

        if download_speed and upload_speed:
            result_text = f"🚀 Download Speed: {download_speed}\n🚀 Upload Speed: {upload_speed}"
        else:
            result_text = "Speed test result format is not recognized."

        # Send the results as text
        await m.edit(result_text)
    except Exception as e:
        await m.edit(str(e))
