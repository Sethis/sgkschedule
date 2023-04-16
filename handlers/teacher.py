

from typing import Optional

from datetime import datetime, date

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp import ClientSession

from db.models import User
from filters import PrefixFilter, ParseFilter, DefaultTeacherFiler

from tools import texts
from tools import wrapper
from tools import other, samples
from tools import LazyEditing
from tools import Builder, Row, Button
from tools import Parser

router = Router(name="teachers_handler")


@router.callback_query(ParseFilter(prefix="by_teacher"),
                       DefaultTeacherFiler(True))
async def schedule_teacher(message: Message, lazy: LazyEditing,
                           session: AsyncSession, aiohttp_session: ClientSession):

    stmt = select(User.teacher_id).where(User.id == message.from_user.id)
    result = await session.execute(stmt)

    teacher_id = result.scalar()
    teacher_name = other.get_teacher_name_by_id(teacher_id, await wrapper.teacher(message, aiohttp_session))

    current = datetime.now().date()

    await show_teacher_schedule(message, current, teacher_id, teacher_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="by_teacher"),
                       DefaultTeacherFiler(False))
@router.callback_query(ParseFilter(prefix="scbt_change"))
async def by_teacher(callback: CallbackQuery, session: AsyncSession,
                     lazy: LazyEditing, parser: Parser):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="sc_teacher")
    await session.execute(stmt)
    await session.commit()

    if parser.prefix == "scbt_change":
        button = Button("←", prefix="scbt_stop_change", additional=parser.additional)

    else:
        button = Button("←", prefix="stop_change_sc")

    markup = Builder(
        Row(button)
    )

    await lazy.edit(texts.scbt_change_text, reply_markup=markup)


@router.callback_query(ParseFilter(prefix="scbt_stop_change"))
async def scbg_stop_change(callback: CallbackQuery, session: AsyncSession,
                           lazy: LazyEditing, parser: Parser,
                           aiohttp_session: ClientSession):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await schedule_by_teacher(callback, lazy, parser, aiohttp_session)


@router.message(PrefixFilter("sc_teacher"))
async def teacher_for_schedule(message: Message, session: AsyncSession,
                               aiohttp_session: ClientSession):

    current = datetime.now().date()

    teacher = message.text
    teacher_list = await wrapper.teacher(message, aiohttp_session)
    teacher = other.get_teacher_by_name(teacher, teacher_list)

    if teacher is None:
        return await message.answer(texts.error_teacher_insert)

    teacher_id = teacher.id
    teacher_name = teacher.name

    stmt = update(User).where(User.id == message.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await show_teacher_schedule(message, current, teacher_id, teacher_name, aiohttp_session)


@router.callback_query(ParseFilter(prefix="sc_by_th"))
async def schedule_by_teacher(callback: CallbackQuery, lazy: LazyEditing,
                              parser: Parser, aiohttp_session: ClientSession):

    additional = parser.additional

    to_date, teacher = additional.split("&")

    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    teacher_id = teacher
    teacher_name = other.get_teacher_name_by_id(teacher_id, await wrapper.teacher(callback, aiohttp_session))

    await show_teacher_schedule(callback, to_date, teacher_id, teacher_name, aiohttp_session, lazy)


async def show_teacher_schedule(event: CallbackQuery | Message, to_date: date,
                                teacher: int, teacher_name: str,
                                aiohttp_session: ClientSession,
                                lazy: Optional[LazyEditing] = None):

    schedule = await wrapper.schedule_by_teacher(teacher, to_date, event, aiohttp_session)

    await samples.show_schedule(event=event,
                                to_date=to_date,
                                info_button_text=teacher_name,
                                prefix="sc_by_th",
                                change_button_prefix="scbt_change",
                                additional=f"{teacher}",
                                schedule=schedule,
                                need_group_name=True,
                                lazy=lazy)
