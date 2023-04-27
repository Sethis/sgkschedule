

import calendar

from typing import Optional

from datetime import date, datetime

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base.types import TeacherResponse, LessonResponse, CabinentResponse

from db.models import User

from tools.utils import LazyEditing
from tools.texts import texts
from tools.utils import Button, Row, Builder
from tools.other import other
from tools.help_text import help_text
from tools.fast_parsing import fast_parsing


class Samples:
    @staticmethod
    def html_formating_string(object_name: str):
        if object_name == "Не задано":
            return "<u><b>Не задано</b></u>"

        return f"<b>{object_name}</b>"
    @staticmethod
    async def send_or_edit(event: CallbackQuery | Message, text: str, markup: InlineKeyboardMarkup,
                           lazy: Optional[LazyEditing]):

        if lazy:
            return await lazy.edit(text, reply_markup=markup)

        return await event.answer(text, reply_markup=markup)

    @staticmethod
    async def get_default_group(event: CallbackQuery | Message, session: AsyncSession) -> str:
        stmt = await session.execute(select(User.group_id).where(User.id == event.from_user.id))
        group_id = stmt.scalar()
        group_name = await fast_parsing.get_group_name_by_id(session, group_id)

        return group_name

    @staticmethod
    async def get_default_teacher(event: CallbackQuery | Message, session: AsyncSession) -> str:
        stmt = await session.execute(select(User.teacher_id).where(User.id == event.from_user.id))
        teacher_id = stmt.scalar()

        if teacher_id:
            teacher_dirty_name = await fast_parsing.get_teacher_name_by_id(session, teacher_id)
            return other.get_humanize_teacher_name(teacher_dirty_name)

        else:
            return "Не задано"

    @staticmethod
    async def get_default_office(event: CallbackQuery | Message, session: AsyncSession) -> str:
        stmt = await session.execute(select(User.office_id).where(User.id == event.from_user.id))
        office_id = stmt.scalar()

        if office_id:
            office_dirty_name = await fast_parsing.get_office_name_by_id(session, office_id)
            return other.get_humanize_office_name(office_dirty_name)

        else:
            return "Не задано"

    @staticmethod
    async def show_menu(event: CallbackQuery | Message, session: AsyncSession,
                        lazy: Optional[LazyEditing] = None):

        stmt = await session.execute(select(User.group_id).where(User.id == event.from_user.id))
        group_id = stmt.scalar()

        group_name = await fast_parsing.get_group_name_by_id(session, group_id)
        teacher_name = await Samples.get_default_teacher(event, session)
        office_name = await Samples.get_default_office(event, session)

        group_name = Samples.html_formating_string(group_name)
        teacher_name = Samples.html_formating_string(teacher_name)
        office_name = Samples.html_formating_string(office_name)

        current = datetime.now()

        to_date = other.get_humanize_date(current)

        weekday = other.get_weekday(current)

        markup = Builder(
            Row(
                Button("Расписания:", prefix="schedule_help")
            ),
            Row(
                Button("По кабинету", prefix="by_office"),
                Button("По группе", prefix="by_group")
            ),
            Row(
                Button("По предмету", prefix="by_discipline"),
                Button("По педагогу", prefix="by_teacher")
            ),
            Row(
                Button("Настройки", prefix="settings"),
            )
        )

        text = f"Группа: {group_name}\nПедагог: {teacher_name}\n" \
               f"Кабинет: {office_name}\n\n" \
               f"Дата: <b>{to_date}</b>\nДень недели: <b>{weekday}</b>"

        await Samples.send_or_edit(event, text, markup, lazy)

    @staticmethod
    async def show_schedule(event: CallbackQuery | Message, to_date: date, info_button_text: str,
                            prefix: str, change_button_prefix: str, additional: str,
                            schedule: LessonResponse | TeacherResponse | CabinentResponse,
                            need_group_name: bool, schedule_type: str,
                            object_id: int,
                            lazy: Optional[LazyEditing] = None,
                            ):

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
                Button(f"{human_date}", prefix=f"{schedule_type}_schedule_date", additional=str(object_id)),
                Button("⇨", prefix=prefix, additional=f"{right_date}&{additional}")
            ),
            Row(
                Button(f"{info_button_text}", prefix=change_button_prefix, additional=f"{to_date}&{additional}"),
            )
        )

        await Samples.send_or_edit(event, text, markup, lazy)

    @staticmethod
    async def show_settings(event: CallbackQuery | Message, session: AsyncSession,
                            lazy: Optional[LazyEditing] = None):
        stmt = await session.execute(select(User.group_id).where(User.id == event.from_user.id))
        group_id = stmt.scalar()

        group_name = await fast_parsing.get_group_name_by_id(session, group_id)
        teacher_name = await Samples.get_default_teacher(event, session)
        office_name = await Samples.get_default_office(event, session)

        markup = Builder(
            Row(
                Button("Группа:", "settings_standart_group"),
                Button(group_name, "change_group")
            ),
            Row(
                Button("Кабинет:", "settings_standart_office"),
                Button(office_name, "change_office")
            ),
            Row(
                Button("Педагог:", "settings_standart_teacher"),
                Button(teacher_name, "change_teacher")
            ),
            Row(
                Button("Связаться с разработчиком", url="t.me/colame"),
            ),
            Row(
                Button("⇦", prefix="menu"),
            )
        )

        await Samples.send_or_edit(event, texts.settings_text, markup, lazy)

    @staticmethod
    async def show_schedule_calendar(event: CallbackQuery | Message, lazy: LazyEditing,
                                     month: int, year: int, schedule_type: str,
                                     prefix: str, object_id: int):

        humanize_date = other.get_humanize_calendar_date(month, year)

        weekdays = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
        weekdays_buttons = []
        for day in weekdays:
            weekdays_buttons.append(Button(day, "calendar_weekdays"))

        calendar_buttons = Samples.get_calendar_buttons(month, year, prefix, object_id)

        left_month, left_year = other.get_calendar_work_date(month, year, plus=False)
        right_month, right_year = other.get_calendar_work_date(month, year, plus=True)

        markup = Builder(
            Row(*weekdays_buttons),
            *calendar_buttons,
            Row(
                Button("⇦", "calendar_change", additional=f"{schedule_type}&{left_month}&{left_year}&{object_id}"),
                Button(humanize_date, "calendar_date"),
                Button("⇨", "calendar_change", additional=f"{schedule_type}&{right_month}&{right_year}&{object_id}")
            )
        )

        text = texts.schedule_calendar

        await Samples.send_or_edit(event, text, markup, lazy)

    @staticmethod
    def get_calendar_buttons(month: int, year: int, prefix: str, object_id: int) -> list[Row]:
        current_date = datetime.now().date()

        month_day = calendar.Calendar().itermonthdates(year, month)

        row_list = []
        current_row = []

        for index, day in enumerate(month_day):
            if index % 7 == 0:
                row_list.append(Row(*current_row))
                current_row = []

            if day.month != month:
                current_row.append(
                    Button(" ", "calendar_other_month_day")
                )
                continue
            if day == current_date:
                humanize_day = f"[{day.day}]"
            else:
                humanize_day = str(day.day)

            current_row.append(
                Button(humanize_day, f"{prefix}", additional=f"{day}&{object_id}")
            )

        row_list.append(Row(*current_row))
        return row_list

    @staticmethod
    async def show_help(event: Message | CallbackQuery, position: int, lazy: Optional[LazyEditing] = None):
        help_text_tuple = help_text.value
        current_help_text = help_text_tuple[position]

        if position == 0:
            markup = Builder(
                Row(
                    Button("⇨", "change_help_menu", additional="1")
                )
            )

        elif len(help_text_tuple) - 1 <= position:
            markup = Builder(
                Row(
                    Button("⇦", "change_help_menu", additional=f"{len(help_text_tuple) - 2}")
                )
            )

        else:
            markup = Builder(
                Row(
                    Button("⇦", "change_help_menu", additional=f"{position - 1}"),
                    Button("⇨", "change_help_menu", additional=f"{position + 1}")
                )
            )

        if lazy:
            return await lazy.edit(current_help_text["text"],
                                   reply_markup=markup,
                                   photo_id=current_help_text["id"])

        return await event.answer_photo(photo=current_help_text["id"],
                                        caption=current_help_text["text"],
                                        reply_markup=markup)

samples = Samples()
