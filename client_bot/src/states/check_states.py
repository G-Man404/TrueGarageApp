from aiogram.fsm.state import StatesGroup, State


class CheckStates(StatesGroup):
    start_state = State()
    input_contact_state = State()
    input_call_type_state = State()
    check_order_status_by_vin_state = State()
