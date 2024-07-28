import os

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.models import Services, Appointments, Users
from utils.keyboards import services_kb, get_time_kb
from utils.states import CalendarState
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime

appointment_router = Router()


@appointment_router.callback_query(F.data == 'get_appointment')
async def get_appointment_handler(callback: CallbackQuery):
    await callback.answer()
    services = Services.select()
    await callback.message.answer('🤔 Выберите услугу, на которую хотите записаться',
                                  reply_markup=services_kb(services))


@appointment_router.callback_query(F.data.startswith('get_service'))
async def get_service_handler(callback: CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
    service = Services.get_by_id(int(callback.data.split()[1]))
    await state.update_data(service=service)
    await callback.answer(f'✅ Вы выбрали {service.name}', show_alert=True)
    await dialog_manager.start(CalendarState.choice_appointment, mode=StartMode.RESET_STACK)


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    await manager.done()
    await callback.message.edit_text(f'📅 Вы выбрали дату: {selected_date.strftime("%d/%m/%y")}\n'
                                     f'Теперь выберите время для записи',
                                     reply_markup=get_time_kb(str(selected_date)))


dialog = Dialog(Window(
        Const("Выберите дату для записи"),
        Calendar(id='calendar', on_click=on_date_selected),
        state=CalendarState.choice_appointment,),)
appointment_router.include_router(dialog)


@appointment_router.callback_query(F.data.startswith('get_time'))
async def get_time_handler(callback: CallbackQuery, state: FSMContext):
    cmd, date, time = callback.data.split()
    appointment_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    if appointment_date < datetime.now():
        return await callback.answer('❌ Невозможно записаться на прошедшее время!')
    appointment = Appointments.get_or_none(Appointments.date_time == appointment_date)
    data = await state.get_data()
    if not appointment:
        await state.clear()
        await callback.answer()
        user = Users.get_or_none(Users.user_id == callback.from_user.id)
        Appointments.create(user=user, service=data['service'], date_time=appointment_date)
        await callback.message.answer(f'''✅ Вы успешно записались на услугу {data["service"].name}
📌 Дата и время записи: {appointment_date.strftime("%d/%m/%Y - %H:%M")}''')
        for admin in os.getenv('ADMINS').split(','):
            await callback.bot.send_message(int(admin), f'''🆕 Новая запись!\n
👤 ФИО: {user.fullname}
📱 Номер телефона: {user.phone_number}
📅 Дата и время записи: {appointment_date.strftime("%d/%m/%Y - %H:%M")}''')
    else:
        await callback.answer('❌ Это время для записи уже занято!')
