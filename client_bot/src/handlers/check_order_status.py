import re

from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import requests

from src.states.check_states import CheckStates
from src.core.config import headers, api_url
from src.keyboards.check_keyboard import by_vin_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в TrueGarage бот!")
    await message.answer("Введите vin своего мотоцикла для отслеживания статуса работ: ")
    await state.set_state(CheckStates.check_order_status_by_vin)


@router.message(CheckStates.check_order_status_by_vin)
async def check_status_by_vin(message: Message, state: FSMContext):
    vin = message.text
    response = requests.get(f"{api_url}/api/v1/orders/vin/{vin}", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        if orders:
            for order in orders:
                await message.answer(f"Заказ {order['number']} находится в статусе {order['status']}",
                                     reply_markup=by_vin_kb(vin))
        else:
            await message.answer("Заказов с таким vin не найдено")
    else:
        await message.answer("Произошла ошибка при получении данных о заказах")
    await state.clear()


@router.callback_query(F.data.regexp(re.compile(r'update_by_vin_(\d+)')))
async def update_by_vin(callback: types.CallbackQuery, state: FSMContext):
    vin = callback.data.split("_")[3]
    response = requests.get(f"{api_url}/api/v1/orders/vin/{vin}", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        if orders:
            for order in orders:
                new_text = f"Заказ {order['number']} находится в статусе {order['status']}"
                if new_text != callback.message.text:
                    await callback.message.edit_text(f"Заказ {order['number']} находится в статусе {order['status']}",
                                                     reply_markup=by_vin_kb(vin))
        else:
            await callback.message.edit_text("Заказов с таким vin не найдено")
    else:
        await callback.message.edit_text("Произошла ошибка при получении данных о заказах")
    await state.clear()


@router.callback_query(F.data.regexp(re.compile(r'back_to_start')))
async def back_to_start(callback: types.CallbackQuery, state: FSMContext):
    await start(message=callback.message, state=state)
