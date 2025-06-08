import asyncio
import aiohttp
from aiogram import Bot
from config import BOT_TOKEN, CHANNEL_ID

JIKAN_API = "https://api.jikan.moe/v4/top/anime"

async def get_latest_anime():
    async with aiohttp.ClientSession() as session:
        async with session.get(JIKAN_API) as resp:
            data = await resp.json()
            return data.get("data", [])[:5]  # Oxirgi 5 ta anime

async def send_latest_to_channel():
    bot = Bot(token=BOT_TOKEN)
    latest_animes = await get_latest_anime()
    for anime in latest_animes:
        message = f"✨ {anime['title']}\n🔗 {anime['url']}"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print(f"[Xatolik] {anime['title']} yuborilmadi: {e}")
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(send_latest_to_channel())
