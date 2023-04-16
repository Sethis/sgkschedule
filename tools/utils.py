

import asyncio

from typing import Optional, TypeVar
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from tools import callback_data


class LazyEditing:
    simple_answer = TypeVar("simple_answer", bound=dict)

    def __init__(self, callback: CallbackQuery, in_channel: bool = False):
        self.event = callback
        self.in_channel = in_channel

    @staticmethod
    def answer(text: Optional[str] = None, show_alert: Optional[bool] = None,
               url: Optional[str] = None, cache_time: Optional[int] = None) -> simple_answer:

        return {"text": text, "show_alert": show_alert, "url": url, "cache_time": cache_time}

    async def edit(self, text: str, reply_markup: InlineKeyboardMarkup = None,
                   answer: Optional[simple_answer] = None, parse_mode: Optional[str] = "HTML",
                   entities: Optional[list] = None, disable_web_page_preview: Optional[bool] = None) -> bool:

        message_date = self.event.message.date
        can_edit = datetime.now(tz=message_date.tzinfo) - message_date < timedelta(hours=47)

        if answer:
            await self.event.answer(**answer)

        else:
            await self.event.answer()

        if can_edit or self.in_channel:
            try:
                return await self.event.message.edit_text(text=text, reply_markup=reply_markup,
                                                          parse_mode=parse_mode, entities=entities,
                                                          disable_web_page_preview=disable_web_page_preview)
            except TelegramBadRequest:
                pass

            return False

        await asyncio.sleep(1)

        result = await self.event.message.answer(text=text, reply_markup=reply_markup,
                                                 parse_mode=parse_mode,
                                                 disable_web_page_preview=disable_web_page_preview)

        return bool(result)


class Button:
    text: str
    url: Optional[str]
    callback_data: Optional[str]

    def __init__(self, text: str, prefix: Optional[str] = None, parameter: Optional[str] = None,
                 value: Optional[str] = None, additional: Optional[str] = None, url: Optional[str] = None):
        self.text = text
        self.prefix = prefix
        self.parameter = parameter
        self.value = value
        self.additional = additional
        self.url = url

    def get_buttons(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.text, url=self.url,
                                    callback_data=callback_data(self.prefix, self.parameter,
                                                                self.value, self.additional))


class Row:
    buttons: list[InlineKeyboardButton]

    def __init__(self, *args: Button):
        self.buttons = []

        for button in args:
            self.buttons.append(button.get_buttons())

    def get_rows(self) -> list[InlineKeyboardButton]:
        return self.buttons


class _Builder:
    @staticmethod
    def __call__(*rows: Row, adjust: Optional[int] = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for row in rows:
            builder.row(*row.get_rows())

        if adjust:
            builder.adjust(adjust)

        return builder.as_markup()


Builder = _Builder()
