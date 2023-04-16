

from aiohttp.client_exceptions import ContentTypeError
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
    async def group(event: CallbackQuery | Message, aiohttp_session: ClientSession) -> GroupResponse:
        try:
            async with aiohttp_session.get('https://mfc.samgk.ru/api/groups') as response:
                json = await response.json()

                return GroupResponse(item=json)

        except ContentTypeError:
            await wrapper.send_message_about_exception(event)

        raise Exception("Error in parsing")

    @staticmethod
    async def cabinet(event: CallbackQuery | Message, aiohttp_session: ClientSession) -> CabinentResponse:
        try:
            async with aiohttp_session.get('https://asu.samgk.ru/api/cabs') as response:
                text = await response.text()
                jt: dict = loads(text)

                cabinets = []
                for index, key in enumerate(jt.keys()):
                    cabinets.append(Cabinet(id=index, name=key))

                return CabinentResponse(item=cabinets)

        except ContentTypeError:
            await wrapper.send_message_about_exception(event)

        raise Exception("Error in parsing")

    @staticmethod
    async def teacher(event: CallbackQuery | Message, aiohttp_session: ClientSession) -> TeacherResponse:
        try:
            async with aiohttp_session.get('https://asu.samgk.ru/api/teachers') as response:
                json = await response.json()

                return TeacherResponse(item=json)

        except ContentTypeError:
            await wrapper.send_message_about_exception(event)

        raise Exception("Error in parsing")

    @staticmethod
    async def schedule_by_group(group: int, to_date: str, event: CallbackQuery | Message,
                                aiohttp_session: ClientSession) -> LessonResponse:
        try:
            async with aiohttp_session.get(f'https://asu.samgk.ru/api/schedule/{group}/{to_date}') as response:
                json = await response.json()

                return LessonResponse(**json)

        except ContentTypeError:
            await wrapper.send_message_about_exception(event)

        raise Exception("Error in parsing")

    @staticmethod
    async def schedule_by_teacher(teacher: str, to_date: str, event: CallbackQuery | Message,
                                  aiohttp_session: ClientSession) -> LessonResponse:
        try:
            async with aiohttp_session.get(
                    f'https://asu.samgk.ru//api/schedule/teacher/{to_date}/{teacher}'
            ) as response:
                json = await response.json()

                return LessonResponse(**json)

        except ContentTypeError:
            await wrapper.send_message_about_exception(event)

        raise Exception("Error in parsing")


wrapper = Wrapper()