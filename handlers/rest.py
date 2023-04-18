import random

from aiogram import Router, Bot
from aiogram.filters import Text, ChatMemberUpdatedFilter, JOIN_TRANSITION, ADMINISTRATOR, IS_NOT_MEMBER

from aiogram.types import Message, CallbackQuery, ErrorEvent, ChatMemberUpdated, ReplyKeyboardRemove

from tools import other
from tools import jokes
from tools import texts

router = Router(name="rest")


@router.message(Text("мяу", ignore_case=True))
async def cat_handler(message: Message):
    random_cat = random.choice((jokes.cat1, jokes.cat2, jokes.cat3, jokes.cat4, jokes.cat5, jokes.cat6))

    await message.answer(f"<code>{random_cat}</code>\n\n Он говорит мяу. Мы просто его не слышим")


@router.message(Text("анекдот", ignore_case=True))
async def cat_handler(message: Message):
    random_joke = random.choice((jokes.anek1, jokes.anek2, jokes.anek3))
    await message.answer(f"{random_joke}")


@router.message(Text("я котик", ignore_case=True))
async def cat_handler(message: Message):
    await message.answer("я котик ты котик", reply_markup=ReplyKeyboardRemove())


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions and chat_info.permissions.can_send_messages:
        await bot.send_message(
            chat_id=event.chat.id,
            text="Привет! Спасибо, что добавили меня. На моей практике, это лучшая группа из всех, которые я видел, "
                 "а видел я, как ты понимаешь, довольно много групп. Чтобы я работал, достаточно написать /start ("
                 "новым пользователям бота) или /menu (уже зарегистрированным). Сейчас я не вижу ваши сообщения, "
                 "так что советую админу группы зажать на боте в списке участников беседы и сделать его "
                 "администратором. Спасибо ", reply_markup=other.get_main_keyboard()
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    await bot.send_message(
        chat_id=event.chat.id,
        text="Юху, я теперь администратор и могу делать что хочу.. "
             "Например скидывать котиков... Коооотики.. Люблю котиков... Надеюсь вы тоже, иначе в боте забаню",
        reply_markup=other.get_main_keyboard()
    )


@router.callback_query()
async def menu(callback: CallbackQuery):
    await callback.answer("Кажется, эта кнопка нерабочая. Пожалуйста, сообщи разработчику о том "
                          "где она находится по ссылке: t.me/colame", show_alert=True)


@router.errors()
async def menu(event: ErrorEvent):
    if event.update.callback_query:
        await event.update.callback_query.message.answer(texts.error_handler_text)
    if event.update.message:
        await event.update.message.answer(texts.error_handler_text)

    raise event.exception
