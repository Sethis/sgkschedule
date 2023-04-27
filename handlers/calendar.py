

from aiogram import Router
from aiogram.types import CallbackQuery

from filters import ParseFilter

from tools import texts
from tools import LazyEditing
from tools import Parser
from tools import samples

router = Router(name="calendar_handler")


@router.callback_query(ParseFilter(prefix="calendar_other_month_day"))
async def other_day(callback: CallbackQuery):
    await callback.answer(texts.other_calendar_day, show_alert=True)


@router.callback_query(ParseFilter(prefix="calendar_date"))
async def other_day(callback: CallbackQuery):
    await callback.answer(texts.calendar_date, show_alert=True)


@router.callback_query(ParseFilter(prefix="calendar_weekdays"))
async def other_day(callback: CallbackQuery):
    await callback.answer(texts.calendar_weekdays, show_alert=True)


@router.callback_query(ParseFilter(prefix="calendar_change"))
async def calendar_change(callback: CallbackQuery, lazy: LazyEditing, parser: Parser):
    additional = parser.additional.split("&")

    schedule_type = additional[0]
    month = int(additional[1])
    year = int(additional[2])
    object_id = int(additional[3])

    await samples.show_schedule_calendar(
        event=callback, lazy=lazy,
        month=month,
        year=year,
        schedule_type=schedule_type,
        prefix=f"{schedule_type}_calendar",
        object_id=object_id
    )
