

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, CallbackQuery, Message

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from db.models import User
from tools import Parser, LazyEditing, texts


class StackerMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
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
            return await handler(event, data)


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
