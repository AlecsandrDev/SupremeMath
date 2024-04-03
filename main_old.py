from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.enums import ParseMode
import asyncio, logging

from aiogram.fsm.context import FSMContext
from sympy import symbols, Eq, solve, Matrix
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

import keyboards


TOKEN_API = "6811063530:AAEZNhCPYyW_ohwJvj3uWUWbHhSJIGYRjN0"
bot = Bot(TOKEN_API)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class EquationState(StatesGroup):
    waiting_for_equation = State()


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
        # canonical_eq = convert_to_canonical(equation)
        # await message.answer(f"Уравнение в каноническом виде1: {canonical_eq}")
        canonical_eq = convert_equation_to_quadratic(equation)
        await message.answer(canonical_eq)


    dp.message.register(wait_for_equation)


def convert_equation_to_quadratic(equation):
    # Разбиваем уравнение на члены
    terms = equation.split('+')

    # Ищем коэффициенты
    coefficients = {'x^2': 0, 'xy': 0, 'y^2': 0}
    for term in terms:
        if 'x^2' in term:
            coefficients['x^2'] = int(re.findall(r'\d+', term)[0])
        elif 'xy' in term:
            coefficients['xy'] = int(re.findall(r'\d+', term)[0])
        elif 'y^2' in term:
            coefficients['y^2'] = int(re.findall(r'\d+', term)[0])

    # Формируем квадратичную форму
    quadratic_form = f"{coefficients['x^2']}x^2+{coefficients['xy']}xy+{coefficients['y^2']}y^2"

    a = int(coefficients['x^2'])
    b = int(coefficients['xy']) / 2
    c = int(coefficients['y^2'])

    matrix = np.array([[int(a), int(b)], [int(b), int(c)]])
    result = '\n'.join([' '.join(map(str, row)) for row in matrix])

    # print(f"a={a} b={b} c={c}")
    # print(f" Тип данных: a={type(a)} b={type(b)} c={type(c)} matrix={type(matrix)}")
    # print(f"a={coefficients['x^2']} b={coefficients['xy']} c={coefficients['y^2']}")

    return f'Уравнение в каноническом виде: b={quadratic_form}\n Матрица А=\n{result}'



# def convert_to_canonical(equation: str) -> str:
#     parts = re.findall(r"[+-]?\d*\.?\d*[a-z]\^?\d*", equation)
#     A, B, C, D, E, F = 0, 0, 0, 0, 0, 0
#
#     for part in parts:
#         coefficient, term = re.match(r"([+-]?\d*\.?\d*)([a-z]\^?\d*)", part).groups()
#         coefficient = float(coefficient) if coefficient else 1.0
#
#         if term == "x^2":
#             A = coefficient
#         elif term == "xy":
#             B = coefficient
#         elif term == "y^2":
#             C = coefficient
#         elif term == "x":
#             D = coefficient
#         elif term == "y":
#             E = coefficient
#         else:
#             F = coefficient
#
#     canonical_equation = f"{A}X^2 + {B}XY + {C}Y^2 + {D}X + {E}Y + {F} = 0"
#     print(f"a={A} b={B} c={C} d={D} e={E} f={F}")
#
#     return canonical_equation


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







