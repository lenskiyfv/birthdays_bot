from aiogram import Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Birthday
from .answers import answers
from .common import is_record_valid, get_args, str_to_date

router = Router(name="commands-router")


class AddRecord(StatesGroup):
    adding_record = State()


async def is_user_registered(message: Message, session: AsyncSession) -> bool:
    result_request = await session.execute(
        select(User).where(User.user_id == message.from_user.id)
    )
    return bool(result_request.scalar_one_or_none())


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    try:
        await session.merge(User(user_id=message.from_user.id))
        await session.commit()
        await message.answer(
            f"Привет, {message.from_user.first_name}!\n" f"{answers['start']}"
        )
    except IntegrityError:
        await message.answer(answers["registered"])


@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext, session: AsyncSession):
    user = await is_user_registered(message, session)
    if user:
        await message.answer(answers["add"])
        await state.set_state(AddRecord.adding_record)
    else:
        await message.answer(answers["need_register"])
        await state.clear()


@router.message(AddRecord.adding_record)
async def add_record(message: Message, state: FSMContext, session: AsyncSession):
    if message.text and is_record_valid(message.text):
        name, surname, birthday = get_args(message.text)
        birthday = str_to_date(birthday)
        await session.merge(
            Birthday(
                name=name,
                surname=surname,
                birthday=birthday,
                user_id=message.from_user.id,
            )
        )
        await session.commit()
        await message.answer(
            f'Запись "{html.bold(html.quote(message.text))}" добавлена'
        )
    else:
        await message.answer(answers["bad_data"])
    await state.clear()


@router.message(Command("list"))
async def cmd_list(message: Message, session: AsyncSession):
    user = await is_user_registered(message, session)
    if user:
        result_request = await session.execute(
            select(Birthday).where(Birthday.user_id == message.from_user.id)
        )
        records = result_request.scalars().all()
        count = len(records)
        if count != 0:
            answer = "Ваши записи:\n"
            for record in records:
                answer = f"{answer}● {record.name} {record.surname} {record.birthday}\n"
            await message.answer(answer)
        else:
            await message.answer(answers["no_records"])
    else:
        await message.answer(answers["need_register"])


@router.message(Command("delete"))
async def cmd_delete(message: Message, session: AsyncSession):
    user = await is_user_registered(message, session)
    if user:
        try:
            query = (
                select(Birthday)
                .where(Birthday.user_id == message.from_user.id)
                .order_by(Birthday.id.desc())
                .limit(1)
            )
            result_request = await session.execute(query)
            record = result_request.scalars().one()
            delete_result_request = await session.execute(query)
            await session.delete(delete_result_request.scalar())
            await session.commit()
            await message.answer(
                f'Запись "{record.name} {record.surname} {record.birthday}" удалена'
            )
        except NoResultFound:
            await message.answer(answers["no_records"])
    else:
        await message.answer(answers["need_register"])


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(answers["help"])


@router.message(Command("stop"))
async def cmd_stop(message: Message, session: AsyncSession):
    user = await is_user_registered(message, session)
    if user:
        await session.execute(delete(User).where(User.user_id == message.from_user.id))
        await session.commit()
        await message.answer(answers["stop"])
    else:
        await message.answer(answers["need_register"])
