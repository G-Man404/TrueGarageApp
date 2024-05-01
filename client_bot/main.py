import asyncio
from aiogram import Bot, Dispatcher

from src.core.config import token
from src.handlers import check_order_status


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(check_order_status.router,
                       )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())