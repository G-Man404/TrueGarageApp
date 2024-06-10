import re

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import requests

from src.states.check_states import CheckStates
from src.core.config import headers, api_url, admins_id
from src.keyboards.check_keyboard import welcome_kb, back_kb, input_call_kb, choose_order_kb, send_contact_kb
from src.messages.messages import check_order_status_text, welcome_text

router = Router()


async def send_message_to_admin(message, phone_number):
    text = f"Новое сообщение!\nОт: @{message.from_user.username}\nНомер: <a herf='tel:{phone_number}'>{phone_number}</a>\nТекст: {message.text}"
    for admin_id in admins_id:
        try:
            await message.bot.send_message(admin_id, text, parse_mode=ParseMode.HTML)
        except:
            pass

@router.message(F.text.lower() == "на главную")
async def back_to_start(message: Message, state: FSMContext):
    await state.set_state(CheckStates.start_state)
    await start(message=message, state=state)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(welcome_text(), parse_mode=ParseMode.HTML, reply_markup=welcome_kb())
    await state.set_state(CheckStates.start_state)


@router.message(CheckStates.start_state, F.text.lower() == "поиск заказа по vin")
async def input_vin(message: Message, state: FSMContext):
    await state.set_state(CheckStates.check_order_by_vin_state)
    await message.answer("Введите пожалуйста VIN:", reply_markup=back_kb())


@router.message(CheckStates.check_order_by_vin_state)
async def check_orders_by_vin(message: Message, state: FSMContext):
    vin = message.text
    response = requests.get(f"{api_url}/api/v1/orders/vin/{vin}", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        if orders:
            await message.answer("Выберите заказ наряд:", reply_markup=choose_order_kb(orders))
            await state.set_state(CheckStates.check_order_by_number_state)
        else:
            await message.answer("Заказов с таким vin не найдено")
    else:
        await message.answer("Произошла ошибка при получении данных о заказах")


@router.message(CheckStates.start_state, F.text.lower() == "поиск заказа по номеру телефона")
async def input_vin(message: Message, state: FSMContext):
    await state.set_state(CheckStates.check_order_by_contact_state)
    await message.answer("Введите поделитесь своим контактом:", reply_markup=send_contact_kb())


@router.message(CheckStates.check_order_by_contact_state)
async def check_orders_by_number(message: Message, state: FSMContext):
    number = message.contact.phone_number
    response = requests.get(f"{api_url}/api/v1/orders/client_number/{number}", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        if orders:
            await message.answer("Выберите заказ наряд:", reply_markup=choose_order_kb(orders))
            await state.set_state(CheckStates.check_order_by_number_state)
        else:
            await message.answer("Заказов с таким номером не найдено")
    else:
        await message.answer("Произошла ошибка при получении данных о заказах")


@router.callback_query(CheckStates.check_order_by_number_state, F.data.regexp(re.compile(r'order_(\d+)')))
async def check_order_by_number(callback: types.CallbackQuery, state: FSMContext):
    number = callback.data.split("_")[1]
    response = requests.get(f"{api_url}/api/v1/orders/number/{number}", headers=headers)
    if response.status_code == 200:
        order = response.json()
        if order:
            await callback.message.answer(check_order_status_text(order),
                                     parse_mode=ParseMode.HTML,
                                          reply_markup=back_kb())
        else:
            await callback.message.answer("Заказов с таким number не найдено")
    else:
        await callback.message.answer("Произошла ошибка при получении данных о заказах")


@router.message(CheckStates.start_state, F.text.lower() == "заказать звонок")
async def input_contact(message: Message, state: FSMContext):
    await state.set_state(CheckStates.input_contact_state)
    await message.answer("Введите пожалуйста номер телефона:", reply_markup=back_kb())


@router.message(CheckStates.input_contact_state)
async def input_type_call(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(CheckStates.input_call_type_state)
    await message.answer("Выберите причину обращения:", reply_markup=input_call_kb())


@router.message(CheckStates.input_call_type_state)
async def sing_up(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await send_message_to_admin(message, state_data["phone"])
    await message.answer("Ваше обращение принято.", reply_markup=back_kb())
    await state.clear()
