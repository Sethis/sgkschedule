

import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import insert, delete

from aiohttp import ClientSession

from tools import wrapper
from db.models import Group, Teacher, Office


class Background:
    @staticmethod
    async def start(session_pool: async_sessionmaker, aiohttp_session: ClientSession):
        await Background.update_data(session_pool, aiohttp_session)

    @staticmethod
    async def update_data(session_pool: async_sessionmaker, aiohttp_session: ClientSession):
        while True:
            async with session_pool() as session:
                await Background.reset_data(session, aiohttp_session)

            await asyncio.sleep(84600)

    @staticmethod
    async def reset_data(session: AsyncSession, aiohttp_session: ClientSession):
        groups = await wrapper.group(aiohttp_session)
        teachers = await wrapper.teacher(aiohttp_session)
        offices = await wrapper.cabinet(aiohttp_session)

        await session.execute(delete(Group))
        await session.execute(delete(Teacher))
        await session.execute(delete(Office))

        await session.execute(insert(Group), [*groups.item])
        await session.execute(insert(Teacher), [*teachers.item])
        await session.execute(insert(Office), [*offices.item])

        await session.commit()


background = Background()
