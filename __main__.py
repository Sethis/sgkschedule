

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import aiohttp

from aiogram import Bot, Dispatcher

from base.config import config
from db.models import Base

from handlers import menu, group, teacher, admin, rest, office, calendar, discipline, settings

from middlewares.basis import CheckerMiddleware, StackerMiddleware

from tools import background


def add_middleware(dp: Dispatcher, sessionmaker: async_sessionmaker) -> Dispatcher:
    dp.message.middleware(
        CheckerMiddleware()
    )
    dp.message.outer_middleware(
        StackerMiddleware(sessionmaker)
    )

    dp.callback_query.middleware(
        CheckerMiddleware()
    )

    dp.callback_query.outer_middleware(
        StackerMiddleware(sessionmaker)
    )

    return dp


def add_routers(dp: Dispatcher) -> Dispatcher:
    routers = (
        menu,
        group,
        teacher,
        office,
        discipline,
        settings,
        calendar,
        admin,
        rest
    )

    for router in routers:
        dp.include_router(router.router)

    return dp


async def main():
    engine = create_async_engine(url=config.db_url, echo=False, pool_size=35, pool_timeout=15)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    dp = Dispatcher(disable_fsm=True)

    dp = add_routers(dp)
    dp = add_middleware(dp, sessionmaker)

    async with aiohttp.ClientSession() as session:
        tasks = (
            dp.start_polling(bot, aiohttp_session=session),
            background.start(sessionmaker, aiohttp_session=session)
        )
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
