from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    input_fullname = State()
    input_number = State()


class CalendarState(StatesGroup):
    choice_appointment = State()


class AdminState(StatesGroup):
    choice_appointment = State()