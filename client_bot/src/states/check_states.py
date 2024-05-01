from aiogram.fsm.state import StatesGroup, State


class CheckStates(StatesGroup):
    check_type = State()
    check_order_status_by_vin = State()