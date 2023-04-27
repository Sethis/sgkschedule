

from typing import Optional

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from filters import PrefixFilter, ParseFilter

from tools import texts
from tools import fast_parsing
from tools import other
from tools import samples
from tools import LazyEditing
from tools import Parser

router = Router(name="menu_handler")


@router.message(Command(commands=["start"]), flags={"start": True})
async def start_message(message: Message, session: AsyncSession):
    stmt = await session.execute(select(User.prefix).where(User.id == message.from_user.id))
    prefix = stmt.scalar()

    if prefix:
        text = texts.already_start_and_insert_group if prefix == "insert_group" else texts.already_start

        return await message.answer(text, reply_markup=other.get_main_keyboard())

    stmt = insert(User).values(id=message.from_user.id, prefix="insert_group")
    await session.execute(stmt)
    await session.commit()

    await message.answer(texts.start)


@router.message(PrefixFilter("insert_group"))
async def insert_group(message: Message, session: AsyncSession):
    group_id = await fast_parsing.get_group_id_by_name(session, message.text)

    if group_id is None:
        return await message.answer(texts.error_group_insert)

    stmt = update(User).values(group_id=group_id).where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    await message.answer(texts.successfully_insert, reply_markup=other.get_main_keyboard())

    stmt = update(User).values(prefix="menu").where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()


@router.message(Command(commands="menu"), PrefixFilter("menu"))
@router.message(Text(text="Меню"), PrefixFilter("menu"))
async def message_menu(message: Message, session: AsyncSession):
    await samples.show_menu(message, session)


@router.callback_query(ParseFilter(prefix="menu"))
async def callback_menu(callback: CallbackQuery, session: AsyncSession,
                        lazy: Optional[LazyEditing] = None):

    await samples.show_menu(callback, session, lazy)


@router.callback_query(ParseFilter(prefix="schedule_help"))
async def schelp(callback: CallbackQuery):
    await callback.answer(texts.schedule_help, show_alert=True)


@router.callback_query(ParseFilter(prefix="back_to_menu"))
async def stop_change_schedule(callback: CallbackQuery, session: AsyncSession,
                               lazy: LazyEditing):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await samples.show_menu(callback, session, lazy)


@router.message(Text(text="Помощь"), PrefixFilter("menu"))
async def message_menu(message: Message):
    await samples.show_help(message, 0)


@router.callback_query(ParseFilter(prefix="change_help_menu"))
async def schelp(callback: CallbackQuery, parser: Parser, lazy: LazyEditing):
    page_number = int(parser.additional)

    await samples.show_help(callback, page_number, lazy)

