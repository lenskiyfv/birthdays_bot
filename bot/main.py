import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import BOT_TOKEN, PG_DSN
from db.models import init_models
from handlers import commands
from handlers.apsched import send_birthday_messages
from middlewares import DbSessionMiddleware


async def main():
    engine = create_async_engine(url=PG_DSN, echo=True)
    await init_models(engine)
    session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=session))
    dp.include_router(commands.router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_birthday_messages,
        trigger="cron",
        hour=10,
        minute=0,
        start_date=datetime.now(),
        kwargs={"bot": bot, "eng": engine},
    )
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
