import copy


def get_date_fa_from_file_name(file_name):
    import jdatetime
    date = get_date_from_date_str(file_name)
    date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')
    return date_fa


def get_date_from_date_str(file_name):
    import datetime
    file_name = str(file_name)
    year = int(file_name[0:4])
    month = int(file_name[4:6])
    day = int(file_name[6:8])
    date = datetime.date(year=year, month=month, day=day)
    return date


def handle_invalid_discounts(request):
    discount = {
        'lte__90': request.POST.get('un90_disc', 0),
        'gt__90': request.POST.get('up90_disc', 0),
    }
    discount['lte__90'] = int(discount['lte__90']) if discount['lte__90'] is not "" else 0
    discount['gt__90'] = int(discount['gt__90']) if discount['gt__90'] is not "" else 0
    return discount


def get_materials_cost(df):
    costs_in_file = {
        'silicon': float(df.loc[3, 'silicon']),
        'cu': float(df.loc[3, 'cu']),
        'alu': float(df.loc[3, 'alu']),
        'steel': float(df.loc[3, 'steel']),
        'dicast': float(df.loc[3, 'dicast']),
    }
    return costs_in_file


def get_materials_post_payload(request):
    materials = [
        'silicon',
        'cu',
        'alu',
        'steel',
        'dicast'
    ]
    materials_post_data = dict()
    for material in materials:
        materials_post_data[material] = request.POST.get(material)
    return materials_post_data


def remove_comma_from_number(number):
    if type(number) in [int, float]:
        return number
    if type(number) == str:
        return float(number.replace(',', ''))
    return number
