import os

from aiogram import F, Router
from aiogram.types import CallbackQuery
from utils.states import AdminState
from utils.models import Appointments, Users
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime

admin_router = Router()


@admin_router.callback_query(F.data == 'admin')
async def admin_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    if str(callback.from_user.id) in os.getenv('ADMINS').split(','):
        await dialog_manager.start(AdminState.choice_appointment, mode=StartMode.RESET_STACK)


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    await manager.done()
    appointments = []
    for appointment in Appointments.select():
        apdatetime = datetime.strptime(str(appointment.date_time), "%Y-%m-%d %H:%M:%S")
        if apdatetime.date() == selected_date:
            appointments.append(appointment)
    await callback.message.edit_text(f'📅 Вы выбрали дату: {selected_date.strftime("%d/%m/%y")}\n'
                                     f'Ниже записи, которые есть на выбранную дату')
    if not appointments:
        await callback.message.answer('Нет записей на выбранную дату!')
    else:
        for appointment in appointments:
            appointment_date = datetime.strptime(str(appointment.date_time), "%Y-%m-%d %H:%M:%S")
            await callback.message.answer(f'''👤 ФИО: {appointment.user.fullname}
📱 Номер телефона: {appointment.user.phone_number}
📅 Дата и время записи: {appointment_date.strftime("%d/%m/%Y - %H:%M")}
✨ Услуга: {appointment.service.name}''')


dialog = Dialog(Window(
        Const("Выберите дату, за какое число показать записи"),
        Calendar(id='calendar', on_click=on_date_selected),
        state=AdminState.choice_appointment,),)
admin_router.include_router(dialog)


@admin_router.callback_query(F.data=='clients')
async def admin_handler(callback: CallbackQuery):
    if str(callback.from_user.id) in os.getenv('ADMINS').split(','):
        await callback.answer()
        await callback.message.answer('Ниже предоставлен список всех клиентов')
        for user in Users.select():
            await callback.message.answer(f'''👤 ФИО: {user.fullname}
📱 Номер телефона: {user.phone_number}''')
