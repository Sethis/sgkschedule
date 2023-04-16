

from typing import Optional

from datetime import date, datetime, timedelta

from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp import ClientSession

from base.types import Lesson, Teacher
from base.types import GroupResponse, TeacherResponse, LessonResponse, CabinentResponse

from db.models import User

from tools import wrapper, LazyEditing, texts
from tools import Button, Row, Builder

from .const import Const


class Other:
    @staticmethod
    def simpler_group_name(name: Optional[str]) -> Optional[str]:
        if name is None:
            return None

        return name.lower().replace("-", "")

    @staticmethod
    def check_groups_in_groups_list(group: str, groups_list: GroupResponse) -> Optional[int]:
        group = other.simpler_group_name(group)
        item = groups_list.item

        for values in item:
            ido = values.id
            name = other.simpler_group_name(values.name)

            if group == name:
                return ido

    @staticmethod
    def get_group_name_by_id(ido: int, groups_list: GroupResponse) -> str:
        item = groups_list.item

        for values in item:
            group_ido = values.id
            name = values.name

            if group_ido == ido:
                return name

    @staticmethod
    def get_semester(current: datetime) -> int:
        current_month = current.month

        if current_month in range(6, 1):
            return 1
        return 2

    @staticmethod
    def get_weekday(to_date: datetime) -> str:
        current_weekday = to_date.weekday()

        return Const.weekdays[current_weekday]

    @staticmethod
    def get_humanize_date(to_data: date) -> str:
        dt = to_data.strftime("%d.%m")
        return f"{dt}.{to_data.year - 2000}"

    @staticmethod
    def get_lesson_time(to_data: date) -> dict[str, str]:
        if to_data.weekday() == 0:
            return Const.monday_callings

        return Const.callings

    @staticmethod
    def get_work_date(to_date: date, plus: bool):
        while True:
            if plus:
                to_date = to_date + timedelta(days=1)

            else:
                to_date = to_date - timedelta(days=1)

            if to_date.weekday() not in (5, 6):
                return to_date

    @staticmethod
    def get_lesson_text(text: str, lesson: Lesson, to_data: date, need_group_name: bool = False) -> str:
        lesson_time = other.get_lesson_time(to_data)[lesson.num]

        if need_group_name:
            group_name = f" ⏐ <b>{lesson.nameGroup}</b>"

        else:
            group_name = ""

        lesson_text = f"<b>{lesson.num}</b>⏐ <b>{lesson_time}</b>\n" \
                      f"{lesson.title}\n{lesson.teachername}\n<b>{lesson.cab}</b>{group_name}"
        text = f"{text}{lesson_text}\n\n"

        return text

    @staticmethod
    def get_teacher_name_by_id(ido: int, teacher_list: TeacherResponse) -> str:
        item = teacher_list.item

        for values in item:
            teacher_id = values.id
            name = values.name

            if teacher_id == ido:
                return name

    @staticmethod
    def get_teacher_by_name(name: str, teacher_list: TeacherResponse) -> Teacher:
        name = name.lower()

        item = teacher_list.item

        for values in item:
            teacher_name = values.name.lower()

            if name in teacher_name:
                return values

    @staticmethod
    def get_main_keyboard() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardBuilder()
        markup.add(KeyboardButton(text="Меню"))

        return markup.as_markup(resize_keyboard=True)


class Samples:
    @staticmethod
    async def show_menu(event: CallbackQuery | Message, session: AsyncSession,
                        aiohttp_session: ClientSession, lazy: Optional[LazyEditing] = None):
        stmt = await session.execute(select(User.group_id).where(User.id == event.from_user.id))
        group_id = stmt.scalar()

        group_name = other.get_group_name_by_id(group_id, await wrapper.group(event, aiohttp_session))

        stmt = await session.execute(select(User.teacher_id).where(User.id == event.from_user.id))
        teacher = stmt.scalar()

        if teacher:
            teacher_dirty_name = other.get_teacher_name_by_id(teacher, await wrapper.teacher(event, aiohttp_session))
            last_name, first_name, father_name = teacher_dirty_name.split(" ")

            teacher_name = f"<b>{first_name} {father_name}\n</b>"

        else:
            teacher_name = "<b><u>Не задано</u></b>\n"

        current = datetime.now()

        semester = other.get_semester(current)

        to_date = other.get_humanize_date(current)

        weekday = other.get_weekday(current)

        markup = Builder(
            Row(
                Button("Расписание:", prefix="schelp")
            ),
            Row(
                Button("Стандартное", prefix="by_default")
            ),
            Row(
                Button("По педагогу", prefix="by_teacher"),
                Button("По кабинету", prefix="by_cabinet")
            ),
            Row(
                Button("По группе", prefix="by_group"),
                Button("По предмету", prefix="by_discipline")
            ),
            Row(
                Button("Настройки", prefix="settings"),
            )
        )

        text = f"Группа: <b>{group_name}</b>\nУчитель: {teacher_name}" \
               f"Семестр: <b>{semester}</b>\nДата: <b>{to_date}</b>\nДень недели: <b>{weekday}</b>"
        if lazy:
            return await lazy.edit(text, reply_markup=markup)

        return await event.answer(text, reply_markup=markup)

    @staticmethod
    async def show_schedule(event: CallbackQuery | Message, to_date: date, info_button_text: str,
                            prefix: str, change_button_prefix: str, additional: str,
                            schedule: LessonResponse | TeacherResponse | CabinentResponse,
                            need_group_name: bool, lazy: Optional[LazyEditing] = None):

        human_date = other.get_humanize_date(to_date)

        lessons = schedule.lessons

        text = ""

        for lesson in lessons:
            text = other.get_lesson_text(text, lesson, to_date, need_group_name)

        if text == "":
            text = texts.text_when_no_lessons

        left_date = other.get_work_date(to_date, plus=False)
        right_date = other.get_work_date(to_date, plus=True)

        markup = Builder(
            Row(
                Button("⇦", prefix=prefix, additional=f"{left_date}&{additional}"),
                Button(f"{human_date}", prefix="sc_date"),
                Button("⇨", prefix=prefix, additional=f"{right_date}&{additional}")
            ),
            Row(
                Button(f"{info_button_text}", prefix=change_button_prefix, additional=f"{to_date}&{additional}"),
            )
        )

        if lazy:
            return await lazy.edit(text, reply_markup=markup)

        return await event.answer(text, reply_markup=markup)


other = Other()

samples = Samples()
