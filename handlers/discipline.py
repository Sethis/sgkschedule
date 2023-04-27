

from aiogram import Router

from aiogram.types import CallbackQuery

from filters import ParseFilter

router = Router(name="discipline_handler")


@router.callback_query(ParseFilter(prefix="by_discipline"))
async def discipline(callback: CallbackQuery):
    await callback.answer("Эта функция была перенесена на следующее обновление. "
                          "Распространяйте бота и она появится намного быстрее", show_alert=True)
