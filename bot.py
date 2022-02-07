# -*- coding: utf-8 -*-
import logging
import aiogram
import asyncio
import sys
from app import handlers
from app.handlers import common

import configparser #config

from aiogram import Bot, Dispatcher, types, Router

from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand

from aiogram import Bot, Dispatcher, F, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

logger = logging.getLogger('__main__')

available_models_sizes = ["Маленькая","Средняя","Большая"]
available_order_types = ["на заказ", "из библиотеки"]
available_materials_types = ["Под дерево","Пластик"]
available_models_nunbers = [1, 2, 3, 4, 5, 6]

router = Router()

class OrderModel(StatesGroup):
    start = State()
    order_type = State()
    models_number = State()
    file = State()
    models_size = State()
    models_material = State()
    location = State()


@router.message(commands = {"start"})
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.start)
    await message.answer("Начнем?")

@router.message(OrderModel.start, F.text.casefold() == "да")
async def process_order(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.order_type)
    await message.answer(
        f"Модель из библиотеки или на заказ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="из библиотеки"),
                    KeyboardButton(text="на заказ"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

@router.message(OrderModel.order_type, F.text.casefold() == available_order_types[1])
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.models_number)
    await message.answer("Введите номер модели.")


@router.message(OrderModel.order_type, F.text.casefold() == available_order_types[0])
async def process_order(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.file)

    await message.answer(
        "Загрузите файл с моделью в любом формате из предложенных: \n.stl \n.obj \n.amf",
        reply_markup=ReplyKeyboardRemove(),
        #Загрузка файла
    )

@router.message(commands = {"cancel"})
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(OrderModel.file)
async def process_order(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.models_size)

    await message.answer(
        "Введите номер модели из библиотеки.",
        reply_markup=ReplyKeyboardRemove(),
        #Загрузка файла
    )

@router.message(OrderModel.order_type, F.text.casefold() == "На заказ")
async def process_order(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.file)

    await message.answer(
        "Загрузите файл с моделью в любом формате из предложенных: \n.stl \n.obj \n.amf",
        reply_markup=ReplyKeyboardRemove(),
        #Загрузка файла
    )








logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Заказать печать"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)

# Парсинг файла конфигурации
config = configparser.ConfigParser()
config.read("config/bot.ini")

####################################################################################################


#logger.error("Starting bot")

async def main():
    bot = Bot(token=config["Token"]["token"])
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
