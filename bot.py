import logging
import aiogram
import asyncio
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
available_order_types = ["На заказ", "Из библиотеки"]
available_materials_types = ["Под дерево","Пластик"]
available_models_nunbers = [1, 2, 3, 4, 5, 6]

router = Router()

class OrderModel(StatesGroup):
    waiting_for_order_type = State()
    waiting_for_models_number = State()
    waiting_file = State()
    waiting_for_models_size = State()
    waiting_for_models_material = State()
    waiting_for_location = State()


@router.message(commands={"start"})
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.waiting_for_order_type)
    await message.answer(
        f"Модель из библиотеки или на заказ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Из библиотеки"),
                    KeyboardButton(text="На заказ"),
                ]
            ],
            resize_keyboard=True,
        ),
    )
    
@router.message(commands={"cancel"})
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

@router.message(OrderModel.waiting_for_models_number, F.text.casefold() == "Из библиотеки")
async def process_lib(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderModel.waiting_for_models_size)

    await message.reply(
        "Выберите размер модели",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(OrderModel.waiting_file, F.text.casefold() == "На заказ")
async def process_order(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Загрузите файл с моделью в любом формате из предложенных: \n.stl \n.obj \n.amf",
        reply_markup=ReplyKeyboardRemove(),
        #Загрузка файла
    )
    
# Настройка логирования в stdout
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

bot = Bot(token=config["Token"]["token"])
dp = Dispatcher(bot)


logger.error("Starting bot")

# Установка команд бота
set_commands(bot)

if __name__ == '__main__':
   asyncio.get_running_loop(bot)


