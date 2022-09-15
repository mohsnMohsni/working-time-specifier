from random import randint, shuffle

# from _calendar.manager import WorkingsDate
from openpyxl import load_workbook


path = "تخصیص.xlsx"
wb_obj = load_workbook(path)
sheet_obj = wb_obj.active
cell_obj = sheet_obj.cell(row=1, column=1)
print(cell_obj.value)


def generate_random_specifie_time(sum_of_random: int = 8) -> list:
    '''
    Generate list of randoms number that sum of them is specified in range.
    '''

    num_sum, numbers = int(), list()
    for index in range(1, 16):
        n = randint(0, sum_of_random - num_sum)
        numbers.append(n)
        num_sum += n
        if num_sum == sum_of_random:
            numbers += [0] * (16 - index)
            break
    shuffle(numbers)
    return numbers
