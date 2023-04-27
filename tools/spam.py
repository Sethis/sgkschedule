

import asyncio

from aiogram import Bot

from db.models import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from tools.other import other


class Spam:
    @staticmethod
    async def start_spam_all_users(bot: Bot, session: AsyncSession, text: str):
        stmt = select(User.id)

        result = await session.execute(stmt)

        users_list = result.fetchall()

        for index, user in enumerate(users_list):
            await asyncio.sleep(0.5)

            user_id = user[0]

            try:
                await bot.send_message(user_id, text)

            except TelegramForbiddenError:
                pass

            except TelegramBadRequest:
                pass

            print(f"{index}/{len(users_list)}")

    @staticmethod
    async def start_spam_with_update_main_keyboard(bot: Bot, session: AsyncSession, text: str):
        stmt = select(User.id)

        result = await session.execute(stmt)

        users_list = result.fetchall()

        for index, user in enumerate(users_list):
            await asyncio.sleep(0.5)

            user_id = user[0]

            try:
                await bot.send_message(user_id, text, reply_markup=other.get_main_keyboard())

            except TelegramForbiddenError:
                pass

            except TelegramBadRequest:
                pass

            print(f"{index}/{len(users_list)}")


spam = Spam()
