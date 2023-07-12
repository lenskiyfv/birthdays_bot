import datetime
from typing import List

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import engine
from db.models import Birthday


async def get_birthdays(eng: engine) -> List[Birthday]:
    async with eng.connect() as conn:
        query = select(Birthday)
        result = await conn.execute(query)
        return [row for row in result]

def is_birthday_today(record: Birthday) -> bool:
    today = datetime.date.today()
    return (today.day == record.birthday.day) and (today.month == record.birthday.month)

async def send_birthday_message(bot: Bot, user_id: int, name: str, surname: str) -> None:
    message = f"Сегодня отмечает день рождения {name} {surname}"
    await bot.send_message(user_id, message)

async def send_birthday_messages(bot: Bot, eng: engine) -> None:
    birthdays = await get_birthdays(eng)
    for record in birthdays:
        if is_birthday_today(record):
            await send_birthday_message(bot, record.user_id, record.name, record.surname)
