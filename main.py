import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


bot = Bot(token=os.getenv('BOT_TOKEN', '8352932956:AAGM_8H6vnNGpd4oIBfjvFOvu-RpfP8TdYI'))
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


@dp.message(AskQuestion.waiting_for_anonymous_question, F.text)
async def receive_anonymous_question(message: Message, state: FSMContext):
    question_text = message.text or ''
    recipient_chat_id = 1747437942
    try:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_message(
            recipient_chat_id,
            f'Пользователь оставил вопрос анонимно:\n\n{question_text}',
            reply_markup=keyboard
        )
        await message.answer('Ваш вопрос отправлен анонимно.')
    except Exception:
        await message.answer('Не удалось отправить вопрос адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Фото в анонимном вопросе
@dp.message(AskQuestion.waiting_for_anonymous_question, F.photo)
async def receive_anonymous_photo(message: Message, state: FSMContext):
    recipient_chat_id = 1747437942
    try:
        file_id = message.photo[-1].file_id
        caption = message.caption or ''
        prefix = 'Пользователь отправил фото анонимно.'
        full_caption = f'{prefix}\n\n{caption}' if caption else prefix
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_photo(recipient_chat_id, file_id, caption=full_caption, reply_markup=keyboard)
        await message.answer('Ваше фото отправлено анонимно.')
    except Exception:
        await message.answer('Не удалось отправить фото адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Видео в анонимном вопросе
@dp.message(AskQuestion.waiting_for_anonymous_question, F.video)
async def receive_anonymous_video(message: Message, state: FSMContext):
    recipient_chat_id = 1747437942
    try:
        file_id = message.video.file_id
        caption = message.caption or ''
        prefix = 'Пользователь отправил видео анонимно.'
        full_caption = f'{prefix}\n\n{caption}' if caption else prefix
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_video(recipient_chat_id, file_id, caption=full_caption, reply_markup=keyboard)
        await message.answer('Ваше видео отправлено анонимно.')
    except Exception:
        await message.answer('Не удалось отправить видео адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


@dp.callback_query(F.data == 'btn_2')
async def handle_named_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AskQuestion.waiting_for_named_question)
    await callback.message.answer('Введите ваш вопрос. Он будет отправлен вместе с вашим никнеймом (username).')
    await callback.answer()


@dp.message(AskQuestion.waiting_for_named_question, F.text)
async def receive_named_question(message: Message, state: FSMContext):
    question_text = message.text or ''
    recipient_chat_id = 1747437942
    user = message.from_user
    username = f"@{user.username}" if user.username else (user.full_name or str(user.id))
    try:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_message(
            recipient_chat_id,
            f'Вопрос от {username}:\n\n{question_text}',
            reply_markup=keyboard
        )
        await message.answer('Ваш вопрос отправлен с вашим именем.')
    except Exception:
        await message.answer('Не удалось отправить вопрос адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. (Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Документ (несжатое фото/видео) в анонимном вопросе
@dp.message(AskQuestion.waiting_for_anonymous_question, F.document)
async def receive_anonymous_document(message: Message, state: FSMContext):
    recipient_chat_id = 1747437942
    try:
        file_id = message.document.file_id
        mime = (message.document.mime_type or '').lower()
        caption = message.caption or ''
        if mime.startswith('image/'):
            prefix = 'Пользователь отправил несжатое фото анонимно.'
        elif mime.startswith('video/'):
            prefix = 'Пользователь отправил несжатое видео анонимно.'
        else:
            prefix = 'Пользователь отправил файл анонимно.'
        full_caption = f'{prefix}\n\n{caption}' if caption else prefix
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_document(recipient_chat_id, file_id, caption=full_caption, reply_markup=keyboard)
        await message.answer('Ваш файл отправлен анонимно.')
    except Exception:
        await message.answer('Не удалось отправить файл адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Документ (несжатое фото/видео) в вопросе с именем
@dp.message(AskQuestion.waiting_for_named_question, F.document)
async def receive_named_document(message: Message, state: FSMContext):
    recipient_chat_id = 1747437942
    user = message.from_user
    username = f"@{user.username}" if user.username else (user.full_name or str(user.id))
    try:
        file_id = message.document.file_id
        mime = (message.document.mime_type or '').lower()
        caption = message.caption or ''
        if mime.startswith('image/'):
            prefix = f'Несжатое фото от {username}.'
        elif mime.startswith('video/'):
            prefix = f'Несжатое видео от {username}.'
        else:
            prefix = f'Файл от {username}.'
        full_caption = f'{prefix}\n\n{caption}' if caption else prefix
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_document(recipient_chat_id, file_id, caption=full_caption, reply_markup=keyboard)
        await message.answer('Ваш файл отправлен с вашим именем.')
    except Exception:
        await message.answer('Не удалось отправить файл адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. (Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Фото в вопросе с именем
@dp.message(AskQuestion.waiting_for_named_question, F.photo)
async def receive_named_photo(message: Message, state: FSMContext):
    recipient_chat_id = 1747437942
    user = message.from_user
    username = f"@{user.username}" if user.username else (user.full_name or str(user.id))
    try:
        file_id = message.photo[-1].file_id
        caption = message.caption or ''
        prefix = f'Фото от {username}.'
        full_caption = f'{prefix}\n\n{caption}' if caption else prefix
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_photo(recipient_chat_id, file_id, caption=full_caption, reply_markup=keyboard)
        await message.answer('Ваше фото отправлено с вашим именем.')
    except Exception:
        await message.answer('Не удалось отправить фото адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. (Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Видео в вопросе с именем
@dp.message(AskQuestion.waiting_for_named_question, F.video)
async def receive_named_video(message: Message, state: FSMContext):
    recipient_chat_id = 1747437942
    user = message.from_user
    username = f"@{user.username}" if user.username else (user.full_name or str(user.id))
    try:
        file_id = message.video.file_id
        caption = message.caption or ''
        prefix = f'Видео от {username}.'
        full_caption = f'{prefix}\n\n{caption}' if caption else prefix
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Посмотреть', callback_data=f'seen:{message.chat.id}')]]
        )
        await bot.send_video(recipient_chat_id, file_id, caption=full_caption, reply_markup=keyboard)
        await message.answer('Ваше видео отправлено с вашим именем.')
    except Exception:
        await message.answer('Не удалось отправить видео адресату. Убедитесь, что пользователь ранее писал боту, или укажите корректный chat_id. (Если вы видете эту ошибку напишите @Sodacodex)')
    finally:
        await state.clear()


# Обработчик кнопки "Посмотреть" у владельца
@dp.callback_query(F.data.startswith('seen:'))
async def handle_seen(callback: CallbackQuery):
    owner_chat_id = 1747437942
    if callback.from_user.id != owner_chat_id:
        await callback.answer('Эта кнопка недоступна.', show_alert=True)
        return

    try:
        _, chat_id_str = callback.data.split(':', 1)
        target_chat_id = int(chat_id_str)
    except Exception:
        await callback.answer('Ошибка формата данных.', show_alert=True)
        return

    try:
        await bot.send_message(
            target_chat_id,
            'Ваш вопрос был замечен, и в скором времени на него придет ответ. Пожалуйста, ожидайте.'
        )
        # Удаляем кнопку, чтобы не кликали повторно
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        await callback.answer('Уведомление отправлено.', show_alert=False)
    except Exception:
        await callback.answer('Не удалось уведомить отправителя.', show_alert=True)

async def main():
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())


