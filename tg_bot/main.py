from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="YOUR_TOKEN_HERE")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Привет! Я бот-предсказатель. Напиши /predict или задай вопрос.")

@dp.message_handler(commands=["predict"])
async def predict(msg: types.Message):
    await msg.answer("Сегодня удача на твоей стороне.")

@dp.message_handler(commands=["help"])
async def help_cmd(msg: types.Message):
    await msg.answer("Команды:\n/start — начать\n/predict — предсказание\n/help — помощь")

@dp.message_handler(content_types=["photo"])
async def photo_handler(msg: types.Message):
    await msg.answer("Красивая картинка!")

@dp.message_handler()
async def echo(msg: types.Message):
    await msg.answer("Ответ: " + msg.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
