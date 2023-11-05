import os
import speedtest
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

@Client.on_message(filters.command("speedtest") & filters.user(Config.ADMIN))
async def run_speedtest(client: Client, message: Message):
    m = await message.reply_text("⚡️ Running Server Speedtest")

    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        result = st.results.dict()
    except Exception as e:
        await m.edit(str(e))  # Convert exception to string before editing
        return

    m = await m.edit("🔄 Sharing Speedtest Results")

    # Create an inline keyboard with two buttons for text and image options
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Text Results", callback_data="text_results"),
                InlineKeyboardButton("Image Results", callback_data="image_results"),
            ]
        ]
    )

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(result["share"], headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        content = response.content

        path = "speedtest_result.png"  # Provide a local file name
        with open(path, "wb") as file:
            file.write(content)
    except requests.exceptions.RequestException as req_err:
        await m.edit(f"Error downloading: {req_err}")
        return

    await m.edit("Choose how you want to receive the results:", reply_markup=keyboard)

@Client.on_callback_query(filters.regex("text_results"))
async def send_text_results(bot, update):
    user_id = update.from_user.id
    await bot.answer_callback_query(update.id, text="Sending text results...")
    # Extract the text results and send them to the user
    result = get_speedtest_results()
    await bot.send_message(user_id, result)

@Client.on_callback_query(filters.regex("image_results"))
async def send_image_results(bot, update):
    user_id = update.from_user.id
    await bot.answer_callback_query(update.id, text="Sending image results...")
    # Send the image results to the user
    path = "speedtest_result.png"
    await bot.send_photo(user_id, photo=path, caption="SpeedTest Results")

def get_speedtest_results():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        result = st.results.dict()
        download_speed = result["download"] / 1024 / 1024
        upload_speed = result["upload"] / 1024 / 1024
        ping = result["ping"]
        isp = result["client"]["isp"]
        country = result["client"]["country"]
        server_name = result["server"]["name"]
        server_country = result["server"]["country"]
        server_sponsor = result["server"]["sponsor"]
        output = f"""💡 <b>SpeedTest Results</b>
        <u><b>Client:</b></u>
        <b>ISP:</b> {isp}
        <b>Country:</b> {country}
        <u><b>Server:</b></u>
        <b>Name:</b> {server_name}
        <b>Country:</b> {server_country}, {server_sponsor}
        -----------------------------------------------
        ⚡️ <b>Ping:</b> {ping} ms
        🚀 <b>Download Speed:</b> {download_speed:.2f} Mbps
        🚀 <b>Upload Speed:</b> {upload_speed:.2f} Mbps"""
        return output
    except Exception as e:
        return f"Error: {str(e)}"
