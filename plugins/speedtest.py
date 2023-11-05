from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from config import Config

@Client.on_message(filters.command("speedtest") & filters.user(Config.ADMIN))
async def run_speedtest(client: Client, message: Message):
    m = await message.reply_text("⚡️ Running Speedtest")

    # Initialize a WebDriver (You need to install the appropriate WebDriver for your browser)
    driver = webdriver.Chrome()

    # Open the fast.com website
    driver.get("https://fast.com")

    # Wait for the test to complete (adjust this delay as needed)
    time.sleep(30)

    # Find the download speed element
    download_speed_element = driver.find_element_by_id("speed-value")

    # Get the download speed value
    download_speed = download_speed_element.text

    # Click the "Show more info" link to reveal upload speed
    show_more_info_link = driver.find_element_by_id("show-more-details-link")
    show_more_info_link.click()
    time.sleep(5)  # Wait for the upload speed to be displayed

    # Find the upload speed element
    upload_speed_element = driver.find_element_by_id("upload-value")

    # Get the upload speed value
    upload_speed = upload_speed_element.text

    # Capture a screenshot of the speed test results
    driver.save_screenshot("speedtest_result.png")

    # Close the browser
    driver.quit()

    # Send the results as an image
    await m.delete()
    await client.send_photo(
        chat_id=message.chat.id,
        photo="speedtest_result.png",
        caption=f"🚀 Download Speed: {download_speed} Mbps\n🚀 Upload Speed: {upload_speed} Mbps",
    )
