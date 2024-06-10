from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def back_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="На главную")
    return kb.as_markup(resize_keyboard=True)


def choose_order_kb(orders):
    kb = InlineKeyboardBuilder()
    for order in orders:
        kb.button(text=f"№{order['number']} | {order['motorcycle']['model']} | {order['status']}",
                  callback_data=f"order_{order['number']}")
    kb.adjust(1)
    return kb.as_markup()


def send_contact_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Поделиться контактом", request_contact=True)
    kb.button(text="На главную")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def welcome_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Поиск заказа по VIN")
    kb.button(text="Поиск заказа по номеру телефона")
    kb.button(text="Заказать звонок")
    kb.adjust(1)
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