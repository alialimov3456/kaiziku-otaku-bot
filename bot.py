from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, CHANNEL_ID, SUPER_ADMIN_ID
from utils import check_subscription, get_top_anime, get_latest_anime, search_anime
from admin_panel import register_admin_handlers
from database import init_db, save_user
from utils import get_recommendation

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["recommend"])
async def handle_recommendation(message: types.Message):
    anime = get_recommendation()
    await message.answer(anime['formatted_text'], disable_web_page_preview=False)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    await save_user(user_id)
    if not await check_subscription(bot, user_id):
        await message.answer("👋 Botdan foydalanish uchun kanalga obuna bo‘ling!", reply_markup=subs_keyboard())
        return
    await message.answer("🎌 <b>Kaiziku Otaku botiga xush kelibsiz!</b>", reply_markup=main_menu())

@dp.message_handler(lambda msg: msg.text == "🔥 Top 10 Anime")
async def top_anime(message: types.Message):
    data = await get_top_anime()
    await message.answer(data)

@dp.message_handler(lambda msg: msg.text == "🆕 Yangi Anime")
async def latest_anime(message: types.Message):
    data = await get_latest_anime()
    await message.answer(data)

@dp.message_handler(lambda msg: msg.text == "🔍 Qidirish")
async def search_start(message: types.Message):
    await message.answer("🔎 Qidiruv uchun anime nomini yuboring:")

@dp.message_handler(lambda msg: msg.text and not msg.text.startswith("/"))
async def search_result(message: types.Message):
    result = await search_anime(message.text)
    await message.answer(result)

# Admin panellarini ro'yxatdan o'tkazish
register_admin_handlers(dp)

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp, skip_updates=True)