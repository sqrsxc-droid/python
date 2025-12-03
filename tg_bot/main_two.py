from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

bot = Bot(token="YOUR_TOKEN_HERE")
dp = Dispatcher(bot)

user_ids = set()

schedule_text = (
    "Расписание на сегодня:\n"
    "1. Математика\n"
    "2. Русский язык\n"
    "3. История\n"
    "4. Физкультура"
)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user_ids.add(msg.from_user.id)
    await msg.answer("Привет! Чтобы получить расписание, напиши /schedule")

@dp.message_handler(commands=["schedule"])
async def send_schedule(msg: types.Message):
    await msg.answer(schedule_text)

async def send_daily_schedule():
    for uid in user_ids:
        try:
            await bot.send_message(uid, schedule_text)
        except:
            pass

async def on_startup(_):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_schedule, "cron", hour=8, minute=0)
    scheduler.start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
