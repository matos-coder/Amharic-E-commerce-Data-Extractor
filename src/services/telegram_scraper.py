import os
import sys
from dotenv import load_dotenv
import asyncio
from telethon import TelegramClient
import csv

# Load environment variables once
os.environ.clear()
load_dotenv(override=True)

TELEGRAM_APP_ID = os.environ.get('telegram_app_id')
TELEGRAM_API_HASH = os.environ.get("telegram_api_hash")

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=1000):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Get view count (may be None if not available)
        view_count = getattr(message, 'views', None)
        
        # Write the channel title along with other data
        writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path, view_count])


# Initialize the client once
client = TelegramClient('scraping_session', TELEGRAM_APP_ID, TELEGRAM_API_HASH)

async def main():
    # client = TelegramClient('session_name', TELEGRAM_APP_ID, TELEGRAM_API_HASH)
    await client.start()
    
    # Create a directory for media files in the data folder
    media_dir = os.path.join('..', '..', 'data', 'raw', 'photos')
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer in the data/raw folder
    csv_path = os.path.join('..', '..', 'data', 'raw', 'telegram_data.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path', 'View Count'])  # Include channel title in the header
        
        # List of channels to scrape
        channels = [
            "@ZemenExpress",
            "@nevacomputer",
            "@meneshayeofficial",
            "@ethio_brand_collection",
            "@Leyueqa",
            "@sinayelj",
            "@Shewabrand",
            "@helloomarketethiopia",
            "@modernshoppingcenter",
            "@qnashcom"
        ]
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Scraped data from {channel}")

    return

# asyncio.run(main())
with client:
    client.loop.run_until_complete(main())