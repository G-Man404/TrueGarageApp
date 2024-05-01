from aiogram.utils.keyboard import InlineKeyboardBuilder


def by_vin_kb(vin: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="Обновить", callback_data=f"update_by_vin_{vin}")
    kb.button(text="Назад", callback_data="back_to_start")
    return kb.as_markup()
