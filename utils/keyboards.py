from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardButton
from utils.models import Services


def main_menu():
    return InlineKeyboardBuilder().button(text='📅 Записаться', callback_data='get_appointment').as_markup()


def services_kb(services: list[Services]):
    builder = InlineKeyboardBuilder()
    for service in services:
        builder.button(text=service.name, callback_data=f'get_service {service}')
    return builder.adjust(2).as_markup()


def get_time_kb(date: str):
    builder = InlineKeyboardBuilder()
    for i in range(10, 18, 2):
        builder.button(text=f'{i}:00', callback_data=f'get_time {date} {i}:00')
    return builder.as_markup()


def admin_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Вывести записи', callback_data='admin'))
    builder.add(InlineKeyboardButton(text='Вывести список клиентов', callback_data='clients'))
    return builder.adjust(2).as_markup()