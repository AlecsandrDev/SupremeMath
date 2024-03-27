# from sympy import symbols, Eq, solve
# #
# # # Создаем символьные переменные
# # x, y = symbols('x y')
# # A, B, C, D, E, F = symbols('A B C D E F')
# #
# # # Пользователь вводит уравнение
# # eq_str = input("Введите уравнение: ")
# #
# # # Разбиваем уравнение на составляющие
# # terms = eq_str.split('+')
# #
# # # Находим каждый параметр
# # for term in terms:
# #     if 'x^2' in term:
# #         A = term
# #     elif 'xy' in term:
# #         B = term
# #     elif 'y^2' in term:
# #         C = term
# #     elif 'x' in term and '2' in term:
# #         D = term
# #     elif 'y' in term and '2' in term:
# #         E = term
# #     else:
# #         F = term[:-2]
# #
# # # Выводим результаты
# # print("a =", A)
# # print("b =", B)
# # print("c =", C)
# # print("d =", D)
# # print("e =", E)
# # print("f =", F)
import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keyboards

API_TOKEN = '6811063530:AAEZNhCPYyW_ohwJvj3uWUWbHhSJIGYRjN0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


def convert_to_canonical(input_equation):
    pattern = r"(\d*)([A-Za-z])\^2\+(\d*)([A-Za-z])([A-Za-z])y\+(\d*)([A-Za-z])\^2\+(\d*)([A-Za-z])x\+(\d*)([A-Za-z])y\+(\d*)=0"
    matches = re.match(pattern, input_equation)

    if matches:
        A = matches.group(1)
        B = matches.group(3)
        C = matches.group(5)
        D = matches.group(7)
        E = matches.group(9)
        F = matches.group(11)

        A1 = A
        C1 = C
        F1 = F

        canonical_equation = f"{A1}X^2 + {C1}Y^2 + {F1} = 0"
        return canonical_equation
    else:
        return "Invalid input equation format"


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Выберите кривую для преобразования:", reply_markup=keyboards.main_kb)


@dp.message(lambda message: message.text == "Кривая 2-го порядка")
async def process_parabola(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите уравнение кривой второго порядка:")


@dp.message()
async def handle_message(message: types.Message):
    input_equation = message.text
    result = convert_to_canonical(input_equation)
    await message.answer(result)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






