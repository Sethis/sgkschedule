

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
from tools import fast_parsing
from tools import samples
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
    teacher_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)

    current = datetime.now().date()

    await show_teacher_schedule(message, current, teacher_id, teacher_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="by_teacher"),
                       DefaultTeacherFiler(False))
@router.callback_query(ParseFilter(prefix="teachers_schedule_change"))
async def by_teacher(callback: CallbackQuery, session: AsyncSession,
                     lazy: LazyEditing, parser: Parser):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="teachers_schedule")
    await session.execute(stmt)
    await session.commit()

    if parser.prefix == "teachers_schedule_change":
        button = Button("←", prefix="teachers_schedule_stop_change", additional=parser.additional)

    else:
        button = Button("←", prefix="back_to_menu")

    markup = Builder(
        Row(button)
    )

    await lazy.edit(texts.teacher_insert, reply_markup=markup)


@router.callback_query(ParseFilter(prefix="teachers_schedule_stop_change"))
async def stop_change_teacher(callback: CallbackQuery, session: AsyncSession,
                              lazy: LazyEditing, parser: Parser,
                              aiohttp_session: ClientSession):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await schedule_by_teacher(callback, lazy, parser, aiohttp_session, session)


@router.message(PrefixFilter("teachers_schedule"))
async def teacher_for_schedule(message: Message, session: AsyncSession,
                               aiohttp_session: ClientSession):

    current = datetime.now().date()

    teacher_id = await fast_parsing.get_teacher_id_by_name(session, message.text)
    teacher_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)

    if teacher_id is None:
        markup = Builder(
            Row(Button("⇦", prefix="back_to_menu"))
        )
        return await message.answer(texts.error_teacher_insert, reply_markup=markup)

    stmt = update(User).where(User.id == message.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await show_teacher_schedule(message, current, teacher_id, teacher_name, aiohttp_session)


@router.callback_query(ParseFilter(prefix="schedule_by_teacher"))
async def schedule_by_teacher(callback: CallbackQuery, lazy: LazyEditing,
                              parser: Parser, aiohttp_session: ClientSession, session: AsyncSession):

    additional = parser.additional

    to_date, teacher_id = additional.split("&")

    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    teacher_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)

    await show_teacher_schedule(callback, to_date, teacher_id, teacher_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="teachers_schedule_date"))
async def schedule_date(callback: CallbackQuery, lazy: LazyEditing, parser: Parser):
    teachers_id = int(parser.additional)

    current = datetime.now()

    await samples.show_schedule_calendar(
        event=callback, lazy=lazy,
        month=current.month,
        year=current.year,
        schedule_type="teachers",
        prefix="teachers_calendar",
        object_id=teachers_id
    )


@router.callback_query(ParseFilter(prefix="teachers_calendar"))
async def teachers_calendar(callback: CallbackQuery, lazy: LazyEditing, parser: Parser, session: AsyncSession,
                            aiohttp_session: ClientSession):

    dirty_date, teacher_id = parser.additional.split("&")

    to_date = datetime.strptime(dirty_date, "%Y-%m-%d").date()
    teacher_id = teacher_id

    teacher_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)

    await show_teacher_schedule(callback, to_date, teacher_id, teacher_name, aiohttp_session, lazy)


async def show_teacher_schedule(event: CallbackQuery | Message, to_date: date,
                                teacher: int, teacher_name: str,
                                aiohttp_session: ClientSession,
                                lazy: Optional[LazyEditing] = None):

    schedule = await wrapper.schedule_by_teacher(teacher, to_date, event, aiohttp_session)

    await samples.show_schedule(event=event,
                                to_date=to_date,
                                info_button_text=teacher_name,
                                prefix="schedule_by_teacher",
                                change_button_prefix="teachers_schedule_change",
                                additional=f"{teacher}",
                                schedule=schedule,
                                need_group_name=True,
                                schedule_type="teachers",
                                object_id=teacher,
                                lazy=lazy)
