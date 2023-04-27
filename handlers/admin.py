

import sys

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tools import spam
from tools import Const


router = Router(name="admin")


@router.message(Command(commands=["spam"]), F.from_user.id == Const.admin)
async def start_spam(message: Message, session: AsyncSession, bot: Bot):
    text = message.html_text

    spam_text = text.split(" || ")

    await message.answer("Ну, я погнал")

    await spam.start_spam_all_users(bot, session, spam_text[1])

    await message.answer("Готово!!!!!!!")


@router.message(Command(commands=["spamkb"]), F.from_user.id == Const.admin)
async def start_spam(message: Message, session: AsyncSession, bot: Bot):
    text = message.html_text

    spam_text = text.split(" || ")

    await message.answer("Ну, я погнал")

    await spam.start_spam_with_update_main_keyboard(bot, session, spam_text[1])

    await message.answer("Готово!!!!!!!")


@router.message(Command(commands=["kys"]), F.from_user.id == Const.admin)
async def start_spam(message: Message):
    await message.answer("Лан(")

    sys.exit()
