import jdatetime


class Date:
    @classmethod
    def get_date_fa_from_file_name(cls, file_name):
        date = cls.get_date_from_date_str(file_name)
        date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')
        return date_fa

    @classmethod
    def get_date_from_date_str(cls, file_name):
        import datetime
        file_name = str(file_name)
        year = int(file_name[0:4])
        month = int(file_name[4:6])
        day = int(file_name[6:8])
        date = datetime.date(year=year, month=month, day=day)
        return date

    @classmethod
    def get_date_str(cls, date_greg):
        return str(date_greg).replace('-', '')
