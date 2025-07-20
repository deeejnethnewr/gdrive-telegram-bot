import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

# Load from .env or environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot client
app = Client(
    "gdrive_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start command handler
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply(
        "👋 හෙලෝ! මට Google Drive link එකක් එවන්න. මම file එක download කරලා ඔයාට දෙන්නම්."
    )

# Handle Google Drive link messages
@app.on_message(filters.text & ~filters.command("start"))
async def download_gdrive(client, message: Message):
    link = message.text.strip()

    if "drive.google.com" not in link:
        await message.reply("❌ මෙය valid Google Drive link එකක් නොවෙයි.")
        return

    await message.reply("📥 Downloading from Google Drive...")

    try:
        # Use gdown to download the file
        subprocess.run(f"gdown --fuzzy '{link}' -O file", shell=True, check=True)

        await message.reply_document("file")  # Send file to user
        os.remove("file")  # Clean up

    except Exception as e:
        await message.reply(f"⚠️ Download Error:\n`{str(e)}`")

# Start the bot
app.run()
