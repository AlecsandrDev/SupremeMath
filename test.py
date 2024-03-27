import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keyboards
import sympy as sp

API_TOKEN = '6811063530:AAEZNhCPYyW_ohwJvj3uWUWbHhSJIGYRjN0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Выбирите тему:", reply_markup=keyboards.main_kb)


@dp.message(lambda message: message.text == 'Кривая 2-го порядка')
async def process_curve_equation(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите уравнение кривой второго порядка (например, 29x^2+24xy+36y^2+82x-96y-91=0):")


@dp.message()
async def process_curve_equation(message: types.Message):
    equation = message.text
    parts = equation.split('=')
    print(parts)
    equation = parts[0]

    # Шаг 1: Приводим уравнение вида B = Ax^2 + 2Hxy + By^2
    A, B, C, D, E, F, x, y = sp.symbols('A B C D E F x y')
    new_eq = sp.expand(equation)
    await message.answer(f"Шаг 1: Уравнение приводится к виду B = {new_eq}")

    # Шаг 2: Составляем систему уравнений для инвариантов
    A1, C1, F1 = sp.symbols('A1 C1 F1')
    eq1 = A1 + C1 - A - C
    eq2 = A1 * C1 - A * C - B
    eq3 = A * F - B * D
    await message.answer(f"Шаг 2: Система уравнений для инвариантов:\n{eq1}\n{eq2}\n{eq3}")

    # Решаем систему уравнений для инвариантов
    sol = sp.solve((eq1, eq2, eq3), (A1, C1, F1))
    await message.answer(f"Решение системы уравнений: {sol}")

    # Рассчитываем угол альфа
    alpha_rad = sp.atan(sol[C1] / (sol[A1] - sol[A])) / 2
    alpha_deg = sp.deg(alpha_rad)
    await message.answer(f"Угол альфа (a) = {alpha_deg} градусов")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






