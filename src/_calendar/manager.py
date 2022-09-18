from datetime import date

import pandas as pd
from irholiday import irHoliday

from .holidays import jholidays, UPDATE_IN_YEAR


CURRENT_YEAR = 1401


def retrive_data_range(startdate: date, freq: str):
    """Retrive data range of starttime and current time by specify frequency."""

    current_date = date.today()
    dr = pd.date_range(start=startdate, end=current_date, freq=freq)
    converted_to_date = [item.date() for item in dr.to_pydatetime()]
    return converted_to_date


class JalaliHolidaysCalender:
    '''
    Use irHoliday to retrive holiday dates,
    use pandas to retrive friday dates,
    convert holidays to list and write into file.
    '''

    HOLIDAY_CACHE_FILE_SRC = 'src/_calendar/holidays.py'

    def __init__(self) -> None:
        self._calendar = irHoliday()
        self.year = CURRENT_YEAR

    def retrive_jalali_holidays(self) -> list:
        df = self._calendar.get_holidays(self.year)
        jalali_holidays = df.get('date').tolist()
        return jalali_holidays

    def retrive_fridays(self, startdate: date) -> list:
        return retrive_data_range(startdate, 'W-FRI')

    def wrtie_into_file(self) -> None:
        with open(self.HOLIDAY_CACHE_FILE_SRC, 'w') as hd:
            _import = 'import datetime\n\n\n'
            h_lists = self.retrive_jalali_holidays()
            assign_var = 'jholidays = {}'.format(h_lists)
            update_in_year = '\nUPDATE_IN_YEAR = {}'.format(CURRENT_YEAR)
            hd.write(_import + assign_var + update_in_year)


class WorkingsDate:
    """Retrive workings date exclude holidays"""

    @classmethod
    def retrive_total_holidays(cls, fridays_startdate: date) -> list:
        _jh_calander = JalaliHolidaysCalender()
        if CURRENT_YEAR == UPDATE_IN_YEAR:
            return jholidays + _jh_calander.retrive_fridays(fridays_startdate)
        return _jh_calander.retrive_jalali_holidays() + _jh_calander.retrive_fridays(fridays_startdate)

    @classmethod
    def retrive_working_dates(cls, startdate: date = date.today()) -> None:
        comman_dates = set(retrive_data_range(startdate, 'D'))
        friday_dates = set(cls.retrive_total_holidays(startdate))
        return comman_dates - friday_dates


if __name__ == '__main__':
    print(WorkingsDate.retrive_working_dates())
