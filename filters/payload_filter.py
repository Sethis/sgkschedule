

from aiogram.filters import BaseFilter
from aiogram.types import Message

from db.models import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PrefixFilter(BaseFilter):
    def __init__(self, prefix: str):

        self.prefix = prefix

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        stmt = select(User.prefix).where(User.id == message.from_user.id)
        result = await session.execute(stmt)

        if result.scalar() != self.prefix:
            return False

        return True


class DefaultTeacherFiler(BaseFilter):
    def __init__(self, is_bool: bool):

        self.is_bool = is_bool

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        stmt = select(User.teacher_id).where(User.id == message.from_user.id)
        result = await session.execute(stmt)

        if bool(result.scalar()) == self.is_bool:
            return True

        return False
