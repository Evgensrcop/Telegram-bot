from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app import handlers
from app.handlers import common  



class OrderModel(StatesGroup):
    waiting_for_order_type = State()
    waiting_for_models_number = State()
    waiting_for_models_size = State()
    waiting_for_models_material = State()
    waiting_for_location = State()

# Выбор типа заказа
async def start_mes(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for type_o in common.available_order_types:
        keyboard.add(type_o)
    await message.answer("Модель из библиотеки или на заказ?")
    await OrderModel.waiting_for_order_type.set()

# Проверка выбора типа заказа
async def order_type_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in common.available_order_types:
        await message.answer("Пожалуйста, выберите тип услуги используя клавиатуру ниже.")
        return
    await state.update_data(chosen_order_type = message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for number in common.available_models_nunbers:
        keyboard.add(number)
    await OrderModel.next()
    await message.answer("Выберете модель из библиотеки.")

# Выбор размера модели
async def models_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in common.available_models_sizes:
        await message.answer("Пожалуйста, выберите размер модели, используя клавиатуру ниже.\nМаленькая - < 50мм\nСредняя - 50-120мм\nБольшая - > 120mm")
        return
    user_data = await state.get_data()
    