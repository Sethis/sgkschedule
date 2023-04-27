

from typing import Optional

from datetime import datetime, date

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp import ClientSession

from db.models import User
from filters import PrefixFilter, ParseFilter

from tools import texts
from tools import fast_parsing
from tools import samples
from tools import wrapper
from tools import LazyEditing
from tools import Builder, Row, Button
from tools import Parser


router = Router(name="groups_handler")


@router.callback_query(ParseFilter(prefix="by_group"))
async def by_default(callback: CallbackQuery, session: AsyncSession,
                     lazy: LazyEditing, aiohttp_session: ClientSession):

    current = datetime.now().date()

    stmt = await session.execute(select(User.group_id).where(User.id == callback.from_user.id))
    group_id = stmt.scalar()

    group_name = await fast_parsing.get_group_name_by_id(session, group_id)

    await show_group_schedule(callback, current, group_id, group_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="groups_schedule_stop_change"))
async def stop_change_group(callback: CallbackQuery, session: AsyncSession, lazy: LazyEditing,
                            parser: Parser, aiohttp_session: ClientSession):
    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await schedule_by_group(callback, lazy, parser, aiohttp_session, session)


@router.callback_query(ParseFilter(prefix="groups_schedule_change"))
async def by_group(callback: CallbackQuery, session: AsyncSession, lazy: LazyEditing, parser: Parser):
    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="groups_schedule")
    await session.execute(stmt)
    await session.commit()

    if parser.prefix == "groups_schedule_change":
        button = Button("⇦", prefix="groups_schedule_stop_change", additional=parser.additional)

    else:
        button = Button("⇦", prefix="back_to_menu")

    markup = Builder(
        Row(button)
    )

    await lazy.edit(texts.change_group_text, reply_markup=markup)


@router.message(PrefixFilter("groups_schedule"))
async def schedule_group(message: Message, session: AsyncSession, aiohttp_session: ClientSession):
    current = datetime.now().date()

    group_id = await fast_parsing.get_group_id_by_name(session, message.text)
    group_name = await fast_parsing.get_group_name_by_id(session, group_id)

    if group_id is None:
        markup = Builder(
            Row(Button("⇦", prefix="back_to_menu"))
        )
        return await message.answer(texts.error_group_insert, reply_markup=markup)

    stmt = update(User).where(User.id == message.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await show_group_schedule(message, current, group_id, group_name, aiohttp_session)


@router.callback_query(ParseFilter(prefix="schedule_by_group"))
async def schedule_by_group(callback: CallbackQuery, lazy: LazyEditing,
                            parser: Parser, aiohttp_session: ClientSession,
                            session: AsyncSession):

    additional = parser.additional.split("&")

    to_date = additional[0]
    group_id = int(additional[1])

    group_name = await fast_parsing.get_group_name_by_id(session, group_id)

    to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    await show_group_schedule(callback, to_date, group_id, group_name, aiohttp_session, lazy)


@router.callback_query(ParseFilter(prefix="groups_schedule_date"))
async def schedule_date(callback: CallbackQuery, lazy: LazyEditing, parser: Parser):
    group_id = int(parser.additional)

    current = datetime.now()

    await samples.show_schedule_calendar(
        event=callback, lazy=lazy,
        month=current.month,
        year=current.year,
        schedule_type="groups",
        prefix="groups_calendar",
        object_id=group_id
    )


@router.callback_query(ParseFilter(prefix="groups_calendar"))
async def groups_calendar(callback: CallbackQuery, lazy: LazyEditing, parser: Parser, session: AsyncSession,
                          aiohttp_session: ClientSession):

    dirty_date, group_id = parser.additional.split("&")

    to_date = datetime.strptime(dirty_date, "%Y-%m-%d").date()
    group_id = int(group_id)

    group_name = await fast_parsing.get_group_name_by_id(session, group_id)

    await show_group_schedule(callback, to_date, group_id, group_name, aiohttp_session, lazy)


async def show_group_schedule(event: CallbackQuery | Message, to_date: date, group: int, group_name: str,
                              aiohttp_session: ClientSession, lazy: Optional[LazyEditing] = None):
    schedule = await wrapper.schedule_by_group(group, to_date, event, aiohttp_session=aiohttp_session)

    await samples.show_schedule(event, to_date,
                                info_button_text=group_name,
                                prefix="schedule_by_group",
                                change_button_prefix="groups_schedule_change",
                                additional=f"{group}",
                                schedule=schedule,
                                need_group_name=False,
                                schedule_type="groups",
                                object_id=group,
                                lazy=lazy)
