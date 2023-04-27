

import asyncio

from aiohttp.client_exceptions import ContentTypeError, ClientConnectorError
from aiohttp import ClientSession

from json import loads

from base.types import GroupResponse, CabinentResponse, TeacherResponse, Cabinet, LessonResponse

from aiogram.types import CallbackQuery, Message

from tools import texts


class Wrapper:
    @staticmethod
    async def send_message_about_exception(event: Message | CallbackQuery):
        if isinstance(event, Message):
            return await event.answer(texts.wrapping_error_text)

        await event.message.answer(texts.wrapping_error_text)

    @staticmethod
    async def group(aiohttp_session: ClientSession) -> GroupResponse:
        try:
            async with aiohttp_session.get('https://mfc.samgk.ru/api/groups') as response:
                json = await response.json()

                return GroupResponse(item=json)

        except (ContentTypeError, ClientConnectorError):
            await asyncio.sleep(2)

            await Wrapper.group(aiohttp_session)

    @staticmethod
    async def cabinet(aiohttp_session: ClientSession) -> CabinentResponse:
        try:
            async with aiohttp_session.get('https://asu.samgk.ru/api/cabs') as response:
                text = await response.text()
                jt: dict = loads(text)

                cabinets = []
                for index, key in enumerate(jt.keys()):
                    cabinets.append(Cabinet(id=index, name=key))

                return CabinentResponse(item=cabinets)

        except (ContentTypeError, ClientConnectorError):
            await asyncio.sleep(2)

            await Wrapper.cabinet(aiohttp_session)

    @staticmethod
    async def teacher(aiohttp_session: ClientSession) -> TeacherResponse:
        try:
            async with aiohttp_session.get('https://asu.samgk.ru/api/teachers') as response:
                json = await response.json()

                return TeacherResponse(item=json)

        except (ContentTypeError, ClientConnectorError):
            await asyncio.sleep(2)

            await Wrapper.teacher(aiohttp_session)

    @staticmethod
    async def schedule_by_group(group: int, to_date: str, event: CallbackQuery | Message,
                                aiohttp_session: ClientSession) -> LessonResponse:
        try:
            async with aiohttp_session.get(f'https://asu.samgk.ru/api/schedule/{group}/{to_date}') as response:
                json = await response.json()

                return LessonResponse(**json)

        except (ContentTypeError, ClientConnectorError):
            await wrapper.send_message_about_exception(event)

        raise ContentTypeError

    @staticmethod
    async def schedule_by_teacher(teacher: str, to_date: str, event: CallbackQuery | Message,
                                  aiohttp_session: ClientSession) -> LessonResponse:
        try:
            async with aiohttp_session.get(
                    f'https://asu.samgk.ru//api/schedule/teacher/{to_date}/{teacher}'
            ) as response:
                json = await response.json()

                return LessonResponse(**json)

        except (ContentTypeError, ClientConnectorError):
            await wrapper.send_message_about_exception(event)

        raise ContentTypeError

    @staticmethod
    async def schedule_by_office(office: str, to_date: str, event: CallbackQuery | Message,
                                 aiohttp_session: ClientSession) -> LessonResponse:
        try:
            async with aiohttp_session.get(
                    f'https://asu.samgk.ru//api/schedule/cabs/{to_date}/cabNum/{office}'
            ) as response:
                json = await response.json()

                return LessonResponse(**json)

        except (ContentTypeError, ClientConnectorError):
            await wrapper.send_message_about_exception(event)

        raise ContentTypeError


wrapper = Wrapper()
