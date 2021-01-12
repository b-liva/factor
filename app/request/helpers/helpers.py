import os
import copy
import pandas as pd
from django.conf import settings

from request.helpers.proforma import ProformaSpec, Proforma


def prepare_data_frame_based_on_proforma_date(date):
    file_name = get_filename_base_on_date(date)
    cost_df = get_cost_dataframe_by_date_str(file_name)
    modified_db = modify_data_frame(cost_df)
    return modified_db, file_name


def adjust_df_materials(modified_df, material_payload):
    df_copy = copy.deepcopy(modified_df)

    modified_df = modify_cost(material_payload, df_copy)

    modified_df = calculate_cost_pandas2(modified_df)
    adjusted_materials = {
        'silicon': int(modified_df.loc[3, 'silicon']),
        'cu': int(modified_df.loc[3, 'cu']),
        'alu': int(modified_df.loc[3, 'alu']),
        'steel': int(modified_df.loc[3, 'steel']),
        'dicast': int(modified_df.loc[3, 'dicast']),
    }
    return {
        'adjusted_df': modified_df,
        'adjusted_materials': adjusted_materials
    }


def modify_cost(payload, df):
    df['silicon'] = payload['silicon']
    df['alu'] = payload['alu']
    df['steel'] = payload['steel']
    df['dicast'] = payload['dicast']
    df['cu'] = payload['cu']
    return df


def calculate_cost_pandas(df):
    df['material_main'] = df['وزن سيليكون استيل'] * df['silicon'] + df['سيم لاكي'] * df['cu'] + df['شمش الومينيوم'] * \
                          df['alu'] + df['وزن قطعات چدني (كامل )'] * df['dicast'] + df['ميلگرد فولادي'] * df['steel']
    df['material_other'] = 0.1 * (df['bearing_cost'] + df['material_main'])
    df['material_total'] = df['material_other'] + df['bearing_cost'] + df['material_main']
    df['cost_overhead'] = df['نرخ سربار'] * df['زمان/ماشين']
    df['cost_wage'] = df['نرخ دستمزد'] * df['زمان /دستمزد']
    df['practical_cost'] = df['material_total'] + df['cost_overhead'] + df['cost_wage']
    df['cost_general'] = 0.5 * df['cost_wage']
    df['cost_calc'] = df['practical_cost'] + df['cost_general'] + df['هزینه بسته بندی']

    return df


def calculate_cost_pandas2(df):
    df['material_main'] = df['وزن سيليكون استيل'] * df['silicon'] + df['سيم لاكي'] * df['cu'] + df['شمش الومينيوم'] * \
                          df['alu'] + df['وزن قطعات چدني (كامل )'] * df['dicast'] + df['ميلگرد فولادي'] * df['steel']
    df['material_other'] = 0.12 * (df['bearing_cost'] + df['material_main'])
    df['material_total'] = df['material_other'] + df['bearing_cost'] + df['material_main']
    df['cost_overhead'] = df['نرخ سربار'] * df['زمان/ماشين']
    df['cost_wage'] = df['نرخ دستمزد'] * df['زمان /دستمزد']
    df['practical_cost'] = df['material_total'] + df['cost_overhead'] + df['cost_wage']
    df['cost_general'] = 0.9 * df['cost_wage']
    df['cost_calc'] = df['practical_cost'] + df['cost_general'] + df['هزینه بسته بندی']

    return df


def get_filename_base_on_date(date):
    date = int(date)
    cost_file_path = os.path.join(settings.PROJECT_DATA_DIR, 'costs')
    files = os.listdir(cost_file_path)
    files_no_ext = [file.split('.')[0] for file in files]
    files_no_ext.sort()

    file_date = files_no_ext[len(files_no_ext) - 1]
    if date < int(files_no_ext[1]):
        return int(files_no_ext[1])
    for file in files_no_ext:
        if date > int(file):
            file_date = file
    return file_date


def modify_data_frame(df):
    if df.iloc[0, 0] == 1:
        df = prepare_data_frame(df)
    else:
        df = prepare_data_frame2(df)
    return df


def get_cost_dataframe_by_date_str(filename):
    cost_file_path = os.path.join(settings.PROJECT_DATA_DIR, f'costs/{filename}.xlsx')
    df_temp = pd.read_excel(cost_file_path)
    return df_temp


def prepare_data_frame(df):
    df.iloc[2, 33] = 'cost'

    df.iloc[2, 0] = df.iloc[1, 0]
    df.iloc[2, 1] = df.iloc[1, 1]
    df.iloc[2, 2] = df.iloc[1, 2]
    df.iloc[2, 3] = df.iloc[1, 3]
    df.iloc[2, 22] = df.iloc[1, 22]
    df.iloc[2, 30] = df.iloc[1, 30]
    df.iloc[2, 31] = df.iloc[1, 31]
    df.iloc[2, 32] = df.iloc[1, 32]
    df.iloc[2, 15] = 'silicon_total'
    df.iloc[2, 16] = 'cu_total'
    df.iloc[2, 17] = 'alu_total'
    df.iloc[2, 18] = 'dicast_total'
    df.iloc[2, 19] = 'steel_total'

    df.columns = df.loc[2]
    df = df.loc[3:69]

    col_names = {
        'POWER(KW)': 'title',
        'قيمت ورق سيليكون استيل': 'silicon',
        'قيمت سيم لاكي': 'cu',
        'قيمت شمش الومينيوم': 'alu',
        ' قيمت قطعات چدني (كامل )': 'dicast',
        'قيمت ميلگرد فولادي': 'steel',
        'قيمت بلبرينگ': 'bearing_cost'
    }

    df.rename(columns=col_names, inplace=True)
    df['bearing_cost'] = df['bearing_cost'].fillna(0)
    df['cost_calc'] = df['cost']
    return df


def prepare_data_frame2(df):
    df.iloc[2, 0:4] = df.iloc[1, 0:4]
    df.iloc[2, 46:] = df.iloc[1, 46:]
    df.iloc[2, 49] = 'cost'

    df.iloc[2, 31] = 'silicon_total'
    df.iloc[2, 32] = 'cu_total'
    df.iloc[2, 33] = 'alu_total'
    df.iloc[2, 34] = 'dicast_total'
    df.iloc[2, 35] = 'steel_total'

    df.columns = df.loc[2]
    df = df.loc[3:69]

    col_names = {
        'POWER(KW)': 'title',
        'قيمت ورق سيليكون استيل': 'silicon',
        'قيمت سيم لاكي': 'cu',
        'قيمت شمش الومينيوم': 'alu',
        ' قيمت قطعات چدني (كامل )': 'dicast',
        'قيمت ميلگرد فولادي': 'steel',
        'قيمت بلبرينگ': 'bearing_cost'
    }
    df.rename(columns=col_names, inplace=True)
    df['bearing_cost'] = df['bearing_cost'].fillna(0)
    df['cost_calc'] = df['cost']
    return df


def get_date_str(date_greg):
    return str(date_greg).replace('-', '')
    # return str(10000 * date_greg.year + 100 * date_greg.month + date_greg.day)


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


def calculate_proforma_profit(proforma, discount=None):
    date = proforma.date_fa.togregorian()
    date = get_date_str(date_greg=date)
    specs = proforma.prefspec_set.filter(price__gt=0).all()

    specs_list = [
        {
            'code': spec.code,
            'qty': spec.qty,
            'power': spec.kw,
            'rpm': spec.rpm,
            'voltage': spec.voltage,
            'price': spec.price,
            'im': spec.im,
            'ip': spec.ip,
            'ic': spec.ic,
        } for spec in specs]

    modified_df, cost_file_name = prepare_data_frame_based_on_proforma_date(date)
    specs_profit = ProformaSpec.add_profit_to_specs(modified_df, specs_list, discount_dict=discount)
    specs_profit_split = ProformaSpec.split_specs_if_profit_exists(specs_profit)

    results = Proforma.get_proforma_profit(specs_profit_split['specs_has_profit'])
    return results


def proformas_profit(proformas):
    result = {
        "cost": 0,
        "price": 0,
        "profit": 0,
        "percent": 0,
    }

    items = ['cost', 'price', 'profit']

    for proforma in proformas:
        profit = calculate_proforma_profit(proforma)
        for item in items:
            result[item] += profit[item]
    if result['cost']:
        result['percent'] = 100 * (result['price'] / result['cost'] - 1)
    else:
        result['percent'] = None
    return result
