

from typing import Optional

from datetime import date, datetime

from aiogram.types import Message, CallbackQuery


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base.types import TeacherResponse, LessonResponse, CabinentResponse

from db.models import User

from tools.utils import LazyEditing
from tools.texts import texts
from tools.utils import Button, Row, Builder
from tools.other import other
from tools.other import fast_parsing


class Samples:
    @staticmethod
    async def show_menu(event: CallbackQuery | Message, session: AsyncSession,
                        lazy: Optional[LazyEditing] = None):
        stmt = await session.execute(select(User.group_id).where(User.id == event.from_user.id))
        group_id = stmt.scalar()

        group_name = await fast_parsing.get_group_name_by_id(session, group_id)

        stmt = await session.execute(select(User.teacher_id).where(User.id == event.from_user.id))
        teacher_id = stmt.scalar()

        if teacher_id:
            teacher_dirty_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)
            teacher_name = other.get_humanize_teacher_name(teacher_dirty_name)

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

    @staticmethod
    async def show_settings(event: CallbackQuery | Message, session: AsyncSession,
                            lazy: Optional[LazyEditing] = None):
        stmt = await session.execute(select(User.group_id).where(User.id == event.from_user.id))
        group_id = stmt.scalar()

        group_name = await fast_parsing.get_group_name_by_id(session, group_id)

        stmt = await session.execute(select(User.teacher_id).where(User.id == event.from_user.id))
        teacher_id = stmt.scalar()
        if teacher_id:
            teacher_dirty_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)
            teacher_name = other.get_humanize_teacher_name(teacher_dirty_name)

        else:
            teacher_name = "<b><u>Не задано</u></b>\n"

        markup = Builder(
            Row(
                Button("Связаться с разработчиком", url="t.me/colame"),
            ),
            Row(
                Button("Сменить группу", prefix="change_group"),
                Button("Сменить педагога", prefix="change_teacher"),
            ),
            Row(
                Button("⇦", prefix="menu"),
            )
        )

        text = f"Заданные параметры:\n   Группа: <b>{group_name}</b>\n   Преподаватель: {teacher_name}\n\n" \
               f"Версия бота: {texts.version}"

        if lazy:
            return await lazy.edit(text, reply_markup=markup)

        return await event.answer(text, reply_markup=markup)


samples = Samples()
