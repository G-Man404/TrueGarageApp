import re

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import requests

from src.states.check_states import CheckStates
from src.core.config import headers, api_url, admins_id
from src.keyboards.check_keyboard import by_vin_kb, welcome_kb, back_kb, input_call_kb
from src.messages.messages import check_order_status_text, welcome_text
router = Router()


async def send_message_to_admin(message, phone_number):
    text = f"Новое сообщение!\nОт: @{message.from_user.username}\nНомер: <a herf='tel:{phone_number}'>{phone_number}</a>\nТекст: {message.text}"
    for admin_id in admins_id:
        await message.bot.send_message(admin_id, text, parse_mode=ParseMode.HTML)

@router.message(F.text.lower() == "назад")
async def back_to_start(message: Message, state: FSMContext):
    await state.set_state(CheckStates.start_state)
    await start(message=message, state=state)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(welcome_text(), parse_mode=ParseMode.HTML, reply_markup=welcome_kb())
    await state.set_state(CheckStates.start_state)


@router.message(CheckStates.start_state, F.text.lower() == "поиск заказа по vin")
async def input_vin(message: Message, state: FSMContext):
    await state.set_state(CheckStates.check_order_status_by_vin_state)
    await message.answer("Введите пожалуйста VIN:", reply_markup=back_kb())


@router.message(CheckStates.check_order_status_by_vin_state)
async def check_status_by_vin(message: Message, state: FSMContext):
    vin = message.text
    response = requests.get(f"{api_url}/api/v1/orders/vin/{vin}", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        if orders:
            for order in orders:
                await message.answer(check_order_status_text(order),
                                     reply_markup=by_vin_kb(vin),
                                     parse_mode=ParseMode.HTML)
            await message.answer("Выберите действие: ", reply_markup=back_kb())
        else:
            await message.answer("Заказов с таким vin не найдено")
    else:
        await message.answer("Произошла ошибка при получении данных о заказах")


@router.callback_query(F.data.regexp(re.compile(r'update_by_vin_(\d+)')))
async def update_by_vin(callback: types.CallbackQuery, state: FSMContext):
    vin = callback.data.split("_")[3]
    response = requests.get(f"{api_url}/api/v1/orders/vin/{vin}", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        if orders:
            for order in orders:
                new_text = check_order_status_text(order)
                if new_text != callback.message.text:
                    await callback.message.edit_text(check_order_status_text(order),
                                                     reply_markup=by_vin_kb(vin),
                                                     parse_mode=ParseMode.HTML)
        else:
            await callback.message.edit_text("Заказов с таким vin не найдено")
    else:
        await callback.message.edit_text("Произошла ошибка при получении данных о заказах")


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
