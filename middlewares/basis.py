

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, CallbackQuery, Message

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, update

from db.models import User

from tools import Parser, LazyEditing, texts
from tools import Const

from datetime import datetime, timedelta


class StackerMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ):
        if isinstance(event, CallbackQuery):
            parser = Parser(event.data)
            parser.parse()
            data["parser"] = parser

            data["lazy"] = LazyEditing(event)

        async with self.session_pool() as session:
            data["session"] = session

            if await self.trottling(event, session):
                return

            return await handler(event, data)

    @staticmethod
    async def trottling(event: Message | CallbackQuery, session: AsyncSession) -> bool:
        stmt = select(User.id).where(User.id == event.from_user.id)
        result = await session.execute(stmt)
        user_id = result.fetchone()

        if not user_id:
            return False

        stmt = select(User.last_interaction).where(User.id == event.from_user.id)
        result = await session.execute(stmt)
        last_interaction = result.scalar()

        current_time = datetime.now()
        new_time = current_time + timedelta(seconds=Const.trottle_seconds)

        stmt = update(User).values(last_interaction=new_time).where(User.id == event.from_user.id)
        await session.execute(stmt)
        await session.commit()

        if current_time - last_interaction < timedelta(seconds=Const.trottle_seconds):
            await StackerMiddleware.send_trottle_error(event)
            return True

        return False

    @staticmethod
    async def send_trottle_error(event: Message | CallbackQuery):
        if isinstance(event, Message):
            return

        return await event.answer(texts.trottle_error_text, show_alert=True)


class CheckerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ):
        session: AsyncSession = data["session"]

        stmt = select(User.group_id).where(User.id == event.from_user.id)

        result = await session.execute(stmt)
        user_group = result.fetchone()

        if user_group is None and not get_flag(data, "start"):
            return await self.registration_warrning(event)

        return await handler(event, data)

    @staticmethod
    async def registration_warrning(event: Message | CallbackQuery):
        if isinstance(event, CallbackQuery):
            return await event.answer(texts.not_registr, show_alert=True)

        await event.answer(texts.not_registr)
