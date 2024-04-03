import re
import numpy as np


#Разделение уравнения на составляющие
def split_equation(equation):
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


equation = "29x^2-24xy+36y^2+82x-96y-91=0"
variables = split_equation(equation)

A11, A12, A22, A1, A2, A0 = 0, 0, 0, 0, 0, 0

A11 = int(variables["A11"])
A12 = int(variables["A12"])
A22 = int(variables["A22"])
A1 = int(variables["A1"])
A2 = int(variables["A2"])
A0 = int(variables["A0"])


# Подсчёт t
t = A11 + A22
print(f"t={t}")

# Подсчёт b
matrix_b = [[A11, A12], [A12, A22]]
result_b = '\n'.join(['\t'.join(map(str, row)) for row in matrix_b])
b = (A11*A22) - (A12 * A12)
print(f"b=\n{result_b} = ({A11} * {A22}) - ({A12} * {A12}) = {b}")

# det_a
matrix_det_a = [[A11, A12, A1],
              [A12, A22, A2],
              [A1, A2, A0]]

det = matrix_det_a[0][0] * (matrix_det_a[1][1] * matrix_det_a[2][2] - matrix_det_a[1][2] * matrix_det_a[2][1]) - \
          matrix_det_a[0][1] * (matrix_det_a[1][0] * matrix_det_a[2][2] - matrix_det_a[1][2] * matrix_det_a[2][0]) + \
          matrix_det_a[0][2] * (matrix_det_a[1][0] * matrix_det_a[2][1] - matrix_det_a[1][1] * matrix_det_a[2][0])
result_a = '\n'.join(['\t'.join(map(str, row)) for row in matrix_det_a])

print(f"\n{result_a} = {matrix_det_a[0][0]} * ({matrix_det_a[1][1]} * {matrix_det_a[2][2]} - {matrix_det_a[1][2]} * {matrix_det_a[2][1]}) - {matrix_det_a[0][1]} * ({matrix_det_a[1][0]} * {matrix_det_a[2][2]} - {matrix_det_a[1][2]} * {matrix_det_a[2][0]}) + {matrix_det_a[0][2]} * ({matrix_det_a[1][0]} * {matrix_det_a[2][1]} - {matrix_det_a[1][1]} * {matrix_det_a[2][0]}) = {det}")

# Определение типа графика


if b > 0 and det != 0 and t*det < 0:
    print("Эллипс")
elif b < 0 & det != 0:
    print("Гипербола")
elif b == 0 & det != 0:
    print("Парабола")

