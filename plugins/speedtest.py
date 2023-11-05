import os
import httpx
from pyrogram import Client, filters
from pyrogram.types import Message
import json

@Client.on_message(filters.command("speedtest"))
async def run_speedtest(client: Client, message: Message):
    m = await message.reply_text("⚡️ Running Speedtest")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://www.speedtest.net/api/js/speedtest-config.php")

        if response.status_code == 200:
            config_data = json.loads(response.text)

            download_speed = config_data["download"]["bandwidth"] / 1024 / 1024  # Convert to Mbps
            upload_speed = config_data["upload"]["bandwidth"] / 1024 / 1024  # Convert to Mbps

            result_text = f"🚀 Download Speed: {download_speed:.2f} Mbps\n🚀 Upload Speed: {upload_speed:.2f} Mbps"

            # Send the results as text
            await m.edit(result_text)
        else:
            await m.edit("Failed to fetch speed test data.")
    except Exception as e:
        await m.edit(str(e))

