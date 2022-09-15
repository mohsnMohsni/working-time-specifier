from irholiday import irHoliday


class JalaliHolidaysCalender:
    '''
    Use irHoliday to retrive a dataframes of holiday,
    convert it to list and write into file.
    '''

    def __init__(self, year: int = 1401) -> None:
        self._calendar = irHoliday()
        self.year = year

    def retrive_jalali_holidays(self) -> list():
        df = self._calendar.get_holidays(self.year)
        jalali_holidays = df.get('jalali_date').tolist()
        return jalali_holidays

    def wrtie_into_file(self) -> None:
        with open('holiday/holidays.py', 'w') as hd:
            _import = 'import jdatetime\n\n\n'
            h_lists = self.retrive_jalali_holidays()
            assign_var = 'hd_arr = {}'.format(h_lists)
            hd.write(_import + assign_var)


if __name__ == '__main__':
    JalaliHolidaysCalender().wrtie_into_file()
