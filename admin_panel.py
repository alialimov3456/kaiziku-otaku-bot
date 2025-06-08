from aiogram import types
from config import SUPER_ADMIN_ID

admins = set([SUPER_ADMIN_ID])

def register_admin_handlers(dp):
    @dp.message_handler(commands=['admin'])
    async def admin_panel(message: types.Message):
        if message.from_user.id not in admins:
            await message.answer("❌ Siz admin emassiz!")
            return
        await message.answer("🔐 Admin panel: /add_admin /remove_admin /admins")

    @dp.message_handler(commands=['add_admin'])
    async def add_admin(message: types.Message):
        try:
            uid = int(message.get_args())
            admins.add(uid)
            await message.answer(f"✅ {uid} admin qilindi!")
        except:
            await message.answer("⚠️ Foydalanuvchi ID kiriting!")

    @dp.message_handler(commands=['remove_admin'])
    async def remove_admin(message: types.Message):
        try:
            uid = int(message.get_args())
            admins.discard(uid)
            await message.answer(f"❌ {uid} adminlikdan olib tashlandi!")
        except:
            await message.answer("⚠️ Foydalanuvchi ID kiriting!")

    @dp.message_handler(commands=['admins'])
    async def list_admins(message: types.Message):
        text = "📋 Adminlar:\n" + "\n".join(str(uid) for uid in admins)
        await message.answer(text)