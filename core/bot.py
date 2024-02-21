from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, BaseFilter
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from typing import Union

from core import vk, excel

    
async def run(token: str):

    bot = Bot(token=token)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)

    class StateSearch(StatesGroup):
        run = State()


    class Fsearch(BaseFilter):
        def __init__(self)-> None: 
            self.state = True

        async def __call__(self, message: Message) -> bool:
            return self.state

    SEARCHING = Fsearch() # заглушка на поиск

    def kb_search()-> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text="Поиск")
        return builder.as_markup(resize_keyboard=True)


    def kb_cancel()-> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text="Отмена")
        return builder.as_markup(resize_keyboard=True)


    @dp.message(StateFilter(None), Command('start'))
    async def command_start(message: Message):
        await message.answer(
            text='...',
            reply_markup=kb_search()
        )

    @dp.message(StateFilter(None), F.text=='Поиск', SEARCHING)
    async def message_handler(message: Message, state: FSMContext):

        await state.set_state(StateSearch.run)
        await message.answer(
            text='Для поиска пользователей <i>(Крым, Севастополь)</i> по году окончания школы, введите <b>год окончания школы</b>:',
            parse_mode="HTML",
            reply_markup=kb_cancel()
        )

    @dp.message(StateFilter(None), F.text=='Поиск')
    async def message_handler(message: Message, state: FSMContext):

        await message.answer(
            text='<b>Кто-то уже выполняет поиск, ожидайте</b>',
            parse_mode="HTML"
        )

    @dp.message(StateSearch.run, F.text)
    async def run_search(message: Message, state: FSMContext):

        response = message.text.strip()
        
        if response.isdigit() and len(response)==4:

            await message.answer(
                text='<b>OK</b>\n<i>Начинаем поиск (обычно занимает минут 5)</i>...',
                parse_mode="HTML",
                reply_markup=kb_search()
            )
            await state.clear()

            
            SEARCHING.state = False

            result = await vk.parse_users(int(response))
            table = FSInputFile(excel.create_table(result))
            
            await message.answer_document(
                table,
                caption='<b>Поиск выполнен успешно!</b>',
                parse_mode="HTML"
            )

            SEARCHING.state = True

        elif response=="Отмена":
            await message.answer(
                text='<b>Действие отменено!</b>',
                parse_mode="HTML",
                reply_markup=kb_search()
            )
            await state.clear()

        else:
            await message.answer(
                text='<b>Ошибка</b>\nВведите год <i>(пример 2023)</i>.',
                parse_mode="HTML"
            )

    await dp.start_polling(bot)