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

        variables = convert_equation_to_quadratic(equation)

        A11, A12, A22, A1, A2, A0 = 0, 0, 0, 0, 0, 0

        A11 = int(variables["A11"])
        A12 = int(variables["A12"])
        A22 = int(variables["A22"])
        A1 = int(variables["A1"])
        A2 = int(variables["A2"])
        A0 = int(variables["A0"])

        # Подсчёт t
        t = A11 + A22
        answer_t = f"t={t}"

        # Подсчёт b
        matrix_b = [[A11, A12], [A12, A22]]
        result_b = '\n'.join(['\t'.join(map(str, row)) for row in matrix_b])
        b = (A11 * A22) - (A12 * A12)
        answer_b = f"b=\n{result_b} = ({A11} * {A22}) - ({A12} * {A12}) = {b}"

        # det_a
        matrix_det_a = [[A11, A12, A1],
                        [A12, A22, A2],
                        [A1, A2, A0]]

        det = matrix_det_a[0][0] * (matrix_det_a[1][1] * matrix_det_a[2][2] - matrix_det_a[1][2] * matrix_det_a[2][1]) - \
              matrix_det_a[0][1] * (matrix_det_a[1][0] * matrix_det_a[2][2] - matrix_det_a[1][2] * matrix_det_a[2][0]) + \
              matrix_det_a[0][2] * (matrix_det_a[1][0] * matrix_det_a[2][1] - matrix_det_a[1][1] * matrix_det_a[2][0])
        result_a = '\n'.join(['\t'.join(map(str, row)) for row in matrix_det_a])

        answer_det = f"\n{result_a} = {matrix_det_a[0][0]} * ({matrix_det_a[1][1]} * {matrix_det_a[2][2]} - {matrix_det_a[1][2]} * {matrix_det_a[2][1]}) - {matrix_det_a[0][1]} * ({matrix_det_a[1][0]} * {matrix_det_a[2][2]} - {matrix_det_a[1][2]} * {matrix_det_a[2][0]}) + {matrix_det_a[0][2]} * ({matrix_det_a[1][0]} * {matrix_det_a[2][1]} - {matrix_det_a[1][1]} * {matrix_det_a[2][0]}) = {det}"

        # Определение типа графика

        answer_g = ""

        if b > 0 and det != 0 and t * det < 0:
            answer_g = "Эллипс"
        elif b < 0 & det != 0:
            answer_g = "Гипербола"
        elif b == 0 & det != 0:
            answer_g = "Парабола"

        answer = f"{answer_t}\n\n{answer_b}\n\ndet A={answer_det}\n\nТип графика={answer_g}"

        await message.answer(answer)

    dp.message.register(wait_for_equation)


def convert_equation_to_quadratic(equation):
    equation = equation.replace("-", "+-")  # добавляем плюс перед отрицательными значениями
    pattern = r'\+|='
    terms = re.split(pattern, equation)  # разделяем уравнение на члены по знакам '+' и '='

    variables = {'A11': 0, 'A12': 0, 'A22': 0, 'A1': 0, 'A2': 0, 'A0': 0}

    for term in terms:
        if 'x^2' in term:
            variables['A11'] += int(term.split('x^2')[0])
        elif 'y^2' in term:
            variables['A22'] += int(term.split('y^2')[0])
        elif 'xy' in term:
            variables['A12'] += int(term.split('xy')[0]) / 2
        elif 'x' in term and 'y' not in term:
            variables['A1'] += int(term.replace('x', '')) / 2
        elif 'y' in term and 'x' not in term:
            variables['A2'] += int(term.replace('y', '')) / 2
        else:
            variables['A0'] += int(term)

    return variables


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())