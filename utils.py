import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_ID

async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def subs_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"))
    kb.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_subs"))
    return kb

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔥 Top 10 Anime", callback_data="top"),
        InlineKeyboardButton("🆕 Yangi Anime", callback_data="latest"),
        InlineKeyboardButton("🔍 Qidirish", callback_data="search"),
    )
    return kb

async def get_top_anime():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.jikan.moe/v4/top/anime") as resp:
            data = await resp.json()
            return "\n".join([f"{i+1}. {anime['title']}" for i, anime in enumerate(data['data'][:10])])

async def get_latest_anime():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.jikan.moe/v4/seasons/now") as resp:
            data = await resp.json()
            return "\n".join([f"- {anime['title']}" for anime in data['data'][:10]])

async def search_anime(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.jikan.moe/v4/anime?q={query}") as resp:
            data = await resp.json()
            if data['data']:
                anime = data['data'][0]
                return f"🎬 <b>{anime['title']}</b>\n🔗 {anime['url']}"
            return "🔍 Hech nima topilmadi."

import aiohttp
import random

async def get_recommendation():
    async with aiohttp.ClientSession() as session:
        page = random.randint(1, 10)
        async with session.get(f"https://api.jikan.moe/v4/top/anime?page={page}") as resp:
            data = await resp.json()
            animes = data.get("data", [])
            if not animes:
                return {"formatted_text": "😔 Tavsiya topilmadi."}
            anime = random.choice(animes)
            formatted = f"🎯 <b>Tavsiya:</b> {anime['title']}\n📅 {anime.get('aired', {}).get('from', '???')[:10]}\n🔗 <a href='{anime['url']}'>Havola</a>"
            return {"formatted_text": formatted}
