from typing import Generator
from random import randint, shuffle

from jdatetime import date as j_date, set_locale
from openpyxl import load_workbook

from .._calendar.manager import WorkingsDate


path = "تخصیص.xlsx"
set_locale('fa_IR')


def generate_random_specifie_time(sum_of_random: int = 8) -> list:
    '''
    Generate list of randoms number that sum of them is specified in range.
    '''

    num_sum, numbers = int(), list()
    for index in range(1, 10):
        n = randint(0, sum_of_random - num_sum)
        numbers.append(n)
        num_sum += n
        if num_sum == sum_of_random:
            numbers += [0] * (10 - index)
            break
    shuffle(numbers)
    return numbers


class XlsxHandler:
    '''
    Open xls, retrive one left to last row and init data dpeneds on it then insert row into xls.
    '''

    def __init__(self) -> None:
        self.wb_obj = load_workbook(path)
        self.sheet_obj = self.wb_obj.active
        self.r_data = self.retrive_last_row_data()

    def retrive_last_row_data(self) -> dict:
        one_left_to_last_row = self.sheet_obj[self.sheet_obj.max_row - 1]
        return {i: cell.value for i, cell in enumerate(one_left_to_last_row)}

    def retrive_rows_to_be_filled(self) -> set:
        date_inserted_before  = j_date(*map(int, self.r_data.get(5).split('.')))
        return WorkingsDate.retrive_working_dates(date_inserted_before.togregorian())

    def generate_rows_data(self) -> Generator:
        rows_to_be_filled = list(self.retrive_rows_to_be_filled())
        rows_to_be_filled.sort()
        index = int(self.r_data.get(0))
        for d in rows_to_be_filled:
            r_jalalit_date = j_date.fromtimestamp(int(d.strftime('%s')))
            index += 1
            yield {
                **self.r_data,
                0: index,
                4: r_jalalit_date.jweekday(),
                5: r_jalalit_date.strftime("%Y.%m.%d"),
                **dict(enumerate(generate_random_specifie_time(), 6))
            }

    def init_xls(self) -> None:
        data = self.generate_rows_data()
        index = self.sheet_obj.max_row
        for i, row in enumerate(data):
            self.sheet_obj.insert_rows(index + i)
            for j, cell_value in enumerate(row.values(), 1):
                ws_cell = self.sheet_obj.cell(row=index + i, column=j)
                ws_cell.value = cell_value
        self.wb_obj.save(path)
