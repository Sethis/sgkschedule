

from typing import Optional, Sequence

from datetime import date, datetime, timedelta

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from sqlalchemy import Row

from base.types import Lesson

from .const import Const


class Other:
    @staticmethod
    def simpler_group_name(name: Optional[str]) -> Optional[str]:
        if name is None:
            return None

        return name.lower().replace("-", "")

    @staticmethod
    def check_groups_in_groups_list(group: str, groups_list: Sequence[Row]) -> Optional[int]:
        group = other.simpler_group_name(group)

        for values in groups_list:
            ido = values[0].id
            name = other.simpler_group_name(values[0].name)

            if group == name:
                return ido

    @staticmethod
    def get_weekday(to_date: datetime) -> str:
        current_weekday = to_date.weekday()

        return Const.weekdays[current_weekday]

    @staticmethod
    def get_humanize_date(to_data: date) -> str:
        dt = to_data.strftime("%d.%m")
        return f"{dt}.{to_data.year - 2000}"

    @staticmethod
    def get_humanize_teacher_name(dirty_name: str) -> str:
        split_name = dirty_name.split(" ")
        if len(split_name) == 3:
            return f"{split_name[1]} {split_name[2]}"

        return dirty_name

    @staticmethod
    def get_humanize_office_name(office_name: str) -> str:
        return office_name.replace("_", "/")

    @staticmethod
    def get_humanize_calendar_date(month: int, year: int) -> str:
        if month < 10:
            return f"0{month}.{year}"

        return f"{month}.{year}"

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
    def get_calendar_work_date(month: int, year: int, plus: bool) -> tuple[int, int]:
        if plus:
            month += 1
            if month > 12:
                return 1, year+1

            return month, year

        month -= 1
        if month < 1:
            return 12, year - 1

        return month, year

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
    def get_main_keyboard() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardBuilder()
        markup.add(KeyboardButton(text="Меню"))
        markup.add(KeyboardButton(text="Помощь"))
        markup.adjust(1)

        return markup.as_markup(resize_keyboard=True)


other = Other()
