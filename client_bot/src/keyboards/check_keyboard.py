from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def back_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    return kb.as_markup(resize_keyboard=True)

def by_vin_kb(vin: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="Обновить", callback_data=f"update_by_vin_{vin}")
    return kb.as_markup()


def welcome_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Поиск заказа по VIN")
    kb.button(text="Заказать звонок")
    return kb.as_markup(resize_keyboard=True)


def input_call_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Получить консультацию")
    kb.button(text="Записаться на ТО")
    kb.button(text="Записаться к Александру")
    kb.button(text="Записаться к Андрею")
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)