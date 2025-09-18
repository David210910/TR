import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


bot = Bot(token=os.getenv('BOT_TOKEN', ''))
dp = Dispatcher(storage=MemoryStorage())


class AskQuestion(StatesGroup):
    waiting_for_anonymous_question = State()
    waiting_for_named_question = State()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Анонимно', callback_data='btn_1')],
        [InlineKeyboardButton(text='С именем (твой username будет виден в канале)', callback_data='btn_2')]
    ])
    await message.answer('Привет! выбери как ты хочешь написать вопрос? (бот сделан @Sodacodex)', reply_markup=keyboard)


@dp.callback_query(F.data == 'btn_1')
async def handle_anonymous_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AskQuestion.waiting_for_anonymous_question)
    await callback.message.answer('Введите вопрос, который вы хотели задать:')
    await callback.answer()


@dp.message(AskQuestion.waiting_for_anonymous_question)
async def receive_anonymous_question(message: Message, state: FSMContext):
    question_text = message.text
    recipient_chat_id = 1747437942
    try:
        await bot.send_message(recipient_chat_id, f'Пользователь оставил вопрос анонимно:\n\n{question_text}')
        await message.answer('Ваш вопрос отправлен анонимно.')
    except Exception:
        await message.answer('Не удалось отправить вопрос адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


@dp.callback_query(F.data == 'btn_2')
async def handle_named_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AskQuestion.waiting_for_named_question)
    await callback.message.answer('Введите ваш вопрос. Он будет отправлен вместе с вашим никнеймом (username).')
    await callback.answer()


@dp.message(AskQuestion.waiting_for_named_question)
async def receive_named_question(message: Message, state: FSMContext):
    question_text = message.text
    recipient_chat_id = 1747437942
    user = message.from_user
    username = f"@{user.username}" if user.username else (user.full_name or str(user.id))
    try:
        await bot.send_message(
            recipient_chat_id,
            f'Вопрос от {username}:\n\n{question_text}'
        )
        await message.answer('Ваш вопрос отправлен с вашим именем.')
    except Exception:
        await message.answer('Не удалось отправить вопрос адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. (Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()

async def main():
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())