import os
import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("speedtest"))
async def run_speedtest(client: Client, message: Message):
    m = await message.reply_text("⚡️ Running Speedtest")

    try:
        # Create a SpeedtestClient object
        st = speedtest.Speedtest()

        # Get the best server for testing
        st.get_best_server()

        # Run the download and upload speed tests
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps

        result_text = f"🚀 Download Speed: {download_speed:.2f} Mbps\n🚀 Upload Speed: {upload_speed:.2f} Mbps"

        # Send the results as text
        await m.edit(result_text)
    except Exception as e:
        await m.edit(str(e))
