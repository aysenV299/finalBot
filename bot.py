from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config.config import Config, load_config
from keyboards.set_menu import set_main_menu

import handlers

from models.methods import DatabaseMethods

async def main() -> None:
    configuration: Config = load_config(".env")

    BOT_TOKEN: str = configuration.tg_bot.token

    redis = Redis(
        host=configuration.redis.redis_host,
        port=configuration.redis.redis_port,
        db=configuration.redis.redis_db,
    )

    database = DatabaseMethods()
    database.create_products_table()

    bot: Bot = Bot(
        token=BOT_TOKEN,
        parse_mode="html"
    )

    storage = RedisStorage(redis=redis)

    dp: Dispatcher = Dispatcher(
        bot=bot,
        configuration=configuration,
        storage=storage,
        database=database
    )

    dp.startup.register(set_main_menu)

    dp.include_router(handlers.admin_handlers.router)
    dp.include_router(handlers.user_handlers.router)
    dp.include_router(handlers.other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
