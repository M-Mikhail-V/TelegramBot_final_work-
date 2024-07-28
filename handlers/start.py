import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.models import Users
from utils.states import Registration
from utils.keyboards import main_menu, admin_menu


start_router = Router()


@start_router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext):
    if str(message.from_user.id) in os.getenv('ADMINS').split(','):
         await message.answer(f'👋 Добро пожаловать хозяин!', reply_markup=admin_menu())
    else:
        user = Users.get_or_none(Users.user_id == message.from_user.id)
        if not user:
            await message.answer(f'''👋 Привет, {message.from_user.full_name}
    Чтобы пользоваться нашим ботом, тебе нужно пройти регистрацию\n\n
    Для этого введите своё имя полностью, в формате: Фамилия Имя Отчество''')
            await state.set_state(Registration.input_fullname)
        else:
            await message.answer(f'👋 Привет, {message.from_user.full_name}\n\n'
                                f'Ты находишься в главном меню, чтобы записаться на услугу, нажми на кнопку ниже',
                                reply_markup=main_menu())
