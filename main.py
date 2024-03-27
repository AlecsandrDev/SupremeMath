from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandStart
import asyncio, logging
from sympy import symbols, Eq, solve

import numpy as np
import matplotlib.pyplot as plt

from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import re

import keyboards


TOKEN_API = "6811063530:AAEZNhCPYyW_ohwJvj3uWUWbHhSJIGYRjN0"
bot = Bot(TOKEN_API)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)





@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Выбирите тему:", reply_markup=keyboards.main_kb)


@dp.message(lambda message: message.text == "Кривая 2-го порядка")
async def process_equation(message: types.Message):
    await message.answer("Введите уравнение кривой 2-го порядка:")

    equation = ''

    async def wait_for_equation(m: types.Message):
        nonlocal equation
        equation = m.text
        await m.answer(f"Вы ввели: {equation}")
        # await message.answer(f"A={a}\nB={b}\nC={c}\nD={d}\nE={e}\nF={f}")

        eq = equation
        canonical_eq = convert_to_canonical(eq)
        await message.answer(f"Уравнение в каноническом виде: {canonical_eq}")


    dp.message.register(wait_for_equation)


def convert_to_canonical(equation: str) -> str:
    parts = re.findall(r"[+-]?\d*\.?\d*[a-z]\^?\d*", equation)
    A, B, C, D, E, F = 0, 0, 0, 0, 0, 0

    for part in parts:
        coefficient, term = re.match(r"([+-]?\d*\.?\d*)([a-z]\^?\d*)", part).groups()
        coefficient = float(coefficient) if coefficient else 1.0

        if term == "x^2":
            A = coefficient
        elif term == "xy":
            B = coefficient
        elif term == "y^2":
            C = coefficient
        elif term == "x":
            D = coefficient
        elif term == "y":
            E = coefficient
        else:
            F = coefficient

    canonical_equation = f"{A}X^2 + {B}XY + {C}Y^2 + {D}X + {E}Y + {F} = 0"

    return canonical_equation



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







