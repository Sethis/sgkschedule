

from typing import Optional, Sequence

from datetime import date, datetime, timedelta

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from sqlalchemy import select
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from base.types import Lesson, Teacher
from base.types import GroupResponse, TeacherResponse

from db.models import Group, Teacher

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

    @staticmethod
    def get_humanize_teacher_name(dirty_name: str) -> str:
        split_name = dirty_name.split(" ")
        if len(split_name) == 3:
            return f"<b>{split_name[1]} {split_name[2]}</b>\n"

        return f"<b>{dirty_name}</b>\n"


class FastParsing:
    @staticmethod
    async def get_group_by_id(session: AsyncSession, ido: int) -> Optional[Group]:
        stmt = select(Group).where(Group.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_group_name_by_id(session: AsyncSession, ido: int) -> Optional[str]:
        stmt = select(Group.name).where(Group.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_group_id_by_name(session: AsyncSession, name: str) -> Optional[int]:
        stmt = select(Group)
        result = await session.execute(stmt)
        groups = result.fetchall()
        return Other.check_groups_in_groups_list(name, groups)

    @staticmethod
    async def get_teacher_by_id(session: AsyncSession, ido: int) -> Optional[Teacher]:
        stmt = select(Teacher).where(Teacher.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_teacher_name_by_id(session: AsyncSession, ido: int) -> Optional[str]:
        stmt = select(Teacher.name).where(Teacher.id == ido)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_teacher_id_by_name(session: AsyncSession, name: str) -> Optional[int]:
        stmt = select(Teacher.id).where(Teacher.name.ilike(f"%{name}%"))
        result = await session.execute(stmt)
        return result.scalar()


fast_parsing = FastParsing()

other = Other()
