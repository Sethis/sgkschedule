

from aiogram import Router
from aiogram.types import Message, CallbackQuery

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from filters import PrefixFilter, ParseFilter

from tools import texts
from tools import fast_parsing
from tools import samples
from tools import LazyEditing
from tools import Button, Row, Builder

router = Router(name="settings_handler")


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

    await lazy.edit(texts.change_teacher, reply_markup=markup)


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


@router.callback_query(ParseFilter(prefix="change_office"))
async def change_group(callback: CallbackQuery, session: AsyncSession, lazy: LazyEditing):
    stmt = update(User).where(User.id == callback.from_user.id).values(prefix="change_office")
    await session.execute(stmt)
    await session.commit()

    markup = Builder(
        Row(
            Button("⇦", prefix="stop_change")
        )
    )

    await lazy.edit(texts.change_office, reply_markup=markup)


@router.message(PrefixFilter("change_office"))
async def insert_group(message: Message, session: AsyncSession):
    office_id = await fast_parsing.get_office_id_by_name(session, message.text)

    if office_id is None:
        markup = Builder(
            Row(Button("⇦", prefix="stop_change"))
                )

        return await message.answer(texts.error_office_insert, reply_markup=markup)

    stmt = update(User).values(office_id=office_id).where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    stmt = update(User).values(prefix="menu").where(User.id == message.from_user.id)
    await session.execute(stmt)
    await session.commit()

    await samples.show_settings(message, session)


@router.callback_query(ParseFilter(prefix="settings_standart_group"))
async def change_group(callback: CallbackQuery):
    await callback.answer(texts.settings_info_group, show_alert=True)


@router.callback_query(ParseFilter(prefix="settings_standart_teacher"))
async def change_group(callback: CallbackQuery):
    await callback.answer(texts.settings_info_teacher, show_alert=True)


@router.callback_query(ParseFilter(prefix="settings_standart_office"))
async def change_group(callback: CallbackQuery):
    await callback.answer(texts.settings_info_office, show_alert=True)
