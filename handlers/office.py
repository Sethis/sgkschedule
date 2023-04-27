

from typing import Optional

from datetime import datetime, date

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp import ClientSession

from db.models import User
from filters import PrefixFilter, ParseFilter, DefaultOfficeFiler

from tools import texts
from tools import wrapper
from tools import fast_parsing
from tools import samples
from tools import LazyEditing
from tools import Builder, Row, Button
from tools import Parser
from tools import other

router = Router(name="office_handler")


@router.callback_query(ParseFilter(prefix="by_office"),
                       DefaultOfficeFiler(True))
async def office_schedule(message: Message, lazy: LazyEditing,
                          session: AsyncSession, aiohttp_session: ClientSession):

    stmt = select(User.office_id).where(User.id == message.from_user.id)
    result = await session.execute(stmt)

    office_id = result.scalar()
    office_name = await fast_parsing.get_office_name_by_id(session, office_id)

    current = datetime.now().date()

    await show_office_schedule(message, current, office_id, office_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="by_office"),
                       DefaultOfficeFiler(False))
@router.callback_query(ParseFilter(prefix="office_schedule_change"))
async def by_office(callback: CallbackQuery, session: AsyncSession,
                    lazy: LazyEditing, parser: Parser):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="office_schedule")
    await session.execute(stmt)
    await session.commit()

    if parser.prefix == "office_schedule_change":
        button = Button("←", prefix="office_schedule_stop_change", additional=parser.additional)

    else:
        button = Button("←", prefix="back_to_menu")

    markup = Builder(
        Row(button)
    )

    await lazy.edit(texts.office_insert, reply_markup=markup)


@router.callback_query(ParseFilter(prefix="office_schedule_stop_change"))
async def stop_change_office(callback: CallbackQuery, session: AsyncSession,
                             lazy: LazyEditing, parser: Parser,
                             aiohttp_session: ClientSession):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await schedule_by_office(callback, lazy, parser, aiohttp_session, session)


@router.message(PrefixFilter("office_schedule"))
async def office_for_schedule(message: Message, session: AsyncSession,
                              aiohttp_session: ClientSession):

    current = datetime.now().date()

    teacher_id = await fast_parsing.get_office_id_by_name(session, message.text)
    teacher_name = await fast_parsing.get_office_name_by_id(session, teacher_id)

    if teacher_id is None:
        markup = Builder(
            Row(Button("⇦", prefix="back_to_menu"))
        )
        return await message.answer(texts.error_office_insert, reply_markup=markup)

    stmt = update(User).where(User.id == message.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await show_office_schedule(message, current, teacher_id, teacher_name, aiohttp_session)


@router.callback_query(ParseFilter(prefix="schedule_by_office"))
async def schedule_by_office(callback: CallbackQuery, lazy: LazyEditing,
                             parser: Parser, aiohttp_session: ClientSession, session: AsyncSession):

    additional = parser.additional.split("&")

    to_date = additional[0]
    office_id = int(additional[1])

    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    office_name = await fast_parsing.get_office_name_by_id(session, office_id)

    await show_office_schedule(callback, to_date, office_id, office_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="office_schedule_date"))
async def schedule_date(callback: CallbackQuery, lazy: LazyEditing, parser: Parser):
    office_id = int(parser.additional)

    current = datetime.now()

    await samples.show_schedule_calendar(
        event=callback, lazy=lazy,
        month=current.month,
        year=current.year,
        schedule_type="office",
        prefix="office_calendar",
        object_id=office_id
    )


@router.callback_query(ParseFilter(prefix="office_calendar"))
async def office_calendar(callback: CallbackQuery, lazy: LazyEditing, parser: Parser, session: AsyncSession,
                          aiohttp_session: ClientSession):

    dirty_date, office_id = parser.additional.split("&")

    to_date = datetime.strptime(dirty_date, "%Y-%m-%d").date()
    office_id = int(office_id)

    office_name = await fast_parsing.get_office_name_by_id(session, office_id)

    await show_office_schedule(callback, to_date, office_id, office_name, aiohttp_session, lazy)


async def show_office_schedule(event: CallbackQuery | Message, to_date: date,
                               office: int, office_name: str,
                               aiohttp_session: ClientSession,
                               lazy: Optional[LazyEditing] = None):

    schedule = await wrapper.schedule_by_office(office_name, to_date, event, aiohttp_session)
    office_name = other.get_humanize_office_name(office_name)

    await samples.show_schedule(event=event,
                                to_date=to_date,
                                info_button_text=office_name,
                                prefix="schedule_by_office",
                                change_button_prefix="office_schedule_change",
                                additional=f"{office}",
                                schedule=schedule,
                                need_group_name=True,
                                schedule_type="office",
                                object_id=office,
                                lazy=lazy)
