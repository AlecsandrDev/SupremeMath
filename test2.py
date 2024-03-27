# import re
# import unittest
# from decimal import Decimal
#
#
# def convert_to_canonical(equation):
#     coefficients = {}
#     pattern = re.compile(r'([+-]?\d*)([A-Za-z])\^(\d)')
#
#     matches = re.findall(pattern, equation)
#     for match in matches:
#         coefficient = match[0] if match[0] != '' else '1'
#         variable = match[1]
#         power = match[2]
#         key = f"{variable}{power}"
#         coefficients[key] = int(coefficient)
#
#     A = coefficients.get('x2', 0)
#     B = coefficients.get('xy', 0)
#     C = coefficients.get('y2', 0)
#     D = coefficients.get('x1', 0)
#     E = coefficients.get('y1', 0)
#     F = coefficients.get('', 0)
#
#     A1 = A
#     C1 = C
#     F1 = F
#
#     print(f"a={A} b={B} c={C} d={D} e={E} f={F}")
#
#     return f"{A1}X^2 + {C1}Y^2 + {F1} = 0"
#
# # Пример использования
# equation = "29x^2+24xy+36y^2+82x-96y-91=0"
# canonical_equation = convert_to_canonical(equation)
# print(canonical_equation)


#
# class TestConvertToCanonical(unittest.TestCase):
#     def test_convert_to_canonical(self):
#         input_equation = "Ax^2+2Bxy+Cy^2+2Dx+2Ey+F=0"
#         expected_output = "A1X^2 + C1Y^2 + F1 = 0"
#         self.assertEqual(convert_to_canonical(input_equation), expected_output)
#
#     def test_invalid_input(self):
#         input_equation = "Invalid equation"
#         expected_output = "Invalid input equation format"
#         self.assertEqual(convert_to_canonical(input_equation), expected_output)
#
# if __name__ == '__main__':
#     unittest.main()


import numpy as np

a = 1
b = 2
c = 3
matrix = np.array([[a, b], [b, c]])

def print_matrix(matrix):
    result = '\n'.join([' '.join(map(str, row)) for row in matrix])

    return f'матрица А=\n{result}'

print(print_matrix(matrix))