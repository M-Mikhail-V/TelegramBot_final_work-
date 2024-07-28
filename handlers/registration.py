from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Registration
from utils.models import Users
from utils.keyboards import main_menu
import phonenumbers

registration_router = Router()


@registration_router.message(Registration.input_fullname)
async def input_fullname_handler(message: Message, state: FSMContext):
    if len(message.text.split()) != 3:
        return await message.answer('❌ Ошибка! Введи своё полное имя в формате: Фамилия Имя Отчество')
    fullname = ' '.join(list(map(str.capitalize, message.text.split())))
    await state.update_data(fullname=fullname)
    await state.set_state(Registration.input_number)
    await message.answer(f'✅ Вы ввели: {fullname}\n'
                         f'Теперь введи свой номер телефона в формате: +79002223344')


@registration_router.message(Registration.input_number)
async def input_number_handler(message: Message, state: FSMContext):
    phone = phonenumbers.parse(message.text, 'RU')
    if not phonenumbers.is_valid_number(phone):
        return message.answer('❌ Ошибка! Введён неверный номер телефона, попробуйте ещё раз')
    data = await state.get_data()
    Users.create(user_id=message.from_user.id, fullname=data['fullname'],
                 phone_number=phone.national_number)
    await state.clear()
    await message.answer('✅ Вы успешно зарегистрировались!\n'
                         'Теперь Вы можете записаться на услуги, нажав на кнопку ниже',
                         reply_markup=main_menu())
