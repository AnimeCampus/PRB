import os
import speedtest
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

@Client.on_message(filters.command("speedtest") & filters.user(Config.ADMIN))
async def run_speedtest(client: Client, message: Message):
    m = await message.reply_text("⚡️ Running Server Speedtest")

    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        m = await m.edit("⚡️ Running Download Speedtest..")
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps

        m = await m.edit("⚡️ Running Upload Speedtest...")
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps

        st.get_best_server()
        st.download()
        st.upload()
        result = st.results.dict()
    except Exception as e:
        await m.edit(str(e))  # Convert exception to string before editing
        return

    m = await m.edit("🔄 Sharing Speedtest Results")

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(result["share"], headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        content = response.content

        path = "speedtest_result.png"  # Provide a local file name
        with open(path, "wb") as file:
            file.write(content)
    except requests.exceptions.RequestException as req_err:
        await m.edit(f"Error downloading: {req_err}")
        return

    output = f"""💡 <b>SpeedTest Results</b>
    <u><b>Client:</b></u>
    <b>ISP:</b> {result['client']['isp']}
    <b>Country:</b> {result['client']['country']}
    <u><b>Server:</b></u>
    <b>Name:</b> {result['server']['name']}
    <b>Country:</b> {result['server']['country']}, {result['server']['cc']}
    <b>Sponsor:</b> {result['server']['sponsor']}
    -----------------------------------------------
    ⚡️ <b>Ping:</b> {result['ping']}
    🚀 <b>Download Speed:</b> {download_speed:.2f} Mbps
    🚀 <b>Upload Speed:</b> {upload_speed:.2f} Mbps"""

    msg = await client.send_photo(
        chat_id=message.chat.id, photo=path, caption=output, parse_mode="html"
    )
    os.remove(path)
    await m.delete()
