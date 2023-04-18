

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
from tools import Button, Row, Builder

router = Router(name="menu")


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


@router.callback_query(ParseFilter(prefix="schelp"))
async def schelp(callback: CallbackQuery):
    await callback.answer(texts.schelp, show_alert=True)


@router.callback_query(ParseFilter(prefix="by_discipline"))
async def discipline(callback: CallbackQuery):
    await callback.answer("Будет добавлено, когда пользователей бота станет больше 1000, "
                          "так что делись им с друзьями, котик", show_alert=True)


@router.callback_query(ParseFilter(prefix="by_cabinet"))
async def cabinet(callback: CallbackQuery):
    await callback.answer("Будет добавлено, когда пользователей бота станет больше 1000. "
                          "То есть уже совсем скоро. Помогай мне с этой целью и рекламируй бота друзьям:3",
                          show_alert=True)


@router.callback_query(ParseFilter(prefix="settings"))
async def settings_hangler(callback: CallbackQuery, session: AsyncSession,
                           lazy: LazyEditing):

    await samples.show_settings(callback, session, lazy)


@router.callback_query(ParseFilter(prefix="stop_change"))
async def stop_change(callback: CallbackQuery, session: AsyncSession,
                      lazy: LazyEditing):

    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="menu")
    await session.execute(stmt)
    await session.commit()

    await samples.show_settings(callback, session, lazy)


@router.callback_query(ParseFilter(prefix="change_group"))
async def change_group(callback: CallbackQuery, session: AsyncSession, lazy: LazyEditing):
    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="change_group")
    await session.execute(stmt)
    await session.commit()

    markup = Builder(
        Row(
            Button("⇦", prefix="stop_change")
        )
    )

    await lazy.edit(texts.change_group_text, reply_markup=markup)


@router.message(PrefixFilter("change_group"))
async def insert_group(message: Message, session: AsyncSession):
    group_id = await fast_parsing.get_group_id_by_name(session, message.text)

    if group_id is None:
        markup = Builder(
            Row(Button("⇦", prefix="stop_change"))
                )

        return await message.answer(texts.error_group_insert, reply_markup=markup)

    stmt = update(User).values(group_id=group_id).where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    stmt = update(User).values(prefix="menu").where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    await samples.show_settings(message, session)


@router.callback_query(ParseFilter(prefix="change_teacher"))
async def change_teacher(callback: CallbackQuery, session: AsyncSession, lazy: LazyEditing):
    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="change_teacher")
    await session.execute(stmt)
    await session.commit()

    markup = Builder(
        Row(
            Button("⇦", prefix="stop_change")
            )
    )

    await lazy.edit(texts.scbt_change_text, reply_markup=markup)


@router.message(PrefixFilter("change_teacher"))
async def changing_teacher(message: Message, session: AsyncSession):
    teacher_id = await fast_parsing.get_teacher_id_by_name(session, message.text)

    if teacher_id is None:
        markup = Builder(
            Row(Button("⇦", prefix="stop_change"))
        )
        return await message.answer(texts.error_teacher_insert, reply_markup=markup)

    stmt = update(User).values(teacher_id=teacher_id).where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    stmt = update(User).values(prefix="menu").where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    await samples.show_settings(message, session)
