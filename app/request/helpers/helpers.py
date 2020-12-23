import os
import copy
from django.conf import settings
import pandas as pd


def split_specs_routine_and_not_routine(specs):
    routine_specs = list()
    not_routine_specs = list()
    for spec in specs:
        if spec['power'] <= 450 and (spec['rpm'] in [1000, 1500, 3000]) and spec['voltage'] <= 400:
            routine_specs.append(spec)
        else:
            not_routine_specs.append(spec)
    return {
        'routine_specs': routine_specs,
        'not_routine_specs': not_routine_specs
    }


def add_profit_to_specs(df, specs, discount_dict=None):
    specs_with_profit = list()
    for spec in specs:
        cost = calculate_cost_of_spec(df, **spec)
        if cost:

            profit = calculate_spec_profit_with_discount(cost, spec, discount_dict)
            percent = 100 * profit['profit'] / cost
            pr = {
                'cost': cost,
                'price': profit['price'],
                'profit': profit['profit'],
                'percent': percent
            }
        else:
            pr = {
                'cost': None,
                'price': None,
                'profit': None,
                'percent': None
            }
        spec.update(pr)
        specs_with_profit.append(spec)
    return specs_with_profit


def calculate_spec_profit_with_discount(cost, spec, discount_dict=None):
    discount = 0
    if discount_dict:
        if spec['power'] <= 90:
            discount = discount_dict['lte__90']
        else:
            discount = discount_dict['gt__90']
    price = spec['price'] * (1 - discount / 100)
    profit = price - cost
    return {
        'price': price,
        'profit': profit
    }


def calculate_profit_of_proforma(specs):
    cost_total = 0
    profit_total = 0
    for spec in specs:
        cost_total += spec['cost']
        profit_total += spec['profit']
    if cost_total:
        percent = (profit_total / cost_total) * 100
    else:
        percent = None
    response = {
        'cost': cost_total,
        'profit': profit_total,
        'percent': percent
    }
    return response


def prepare_data_frame_based_on_proforma_date(date):
    file_name = get_filename_base_on_date(date)
    cost_df = get_cost_dataframe_by_date_str(file_name)
    modified_db = modify_data_frame(cost_df)
    return modified_db, file_name


def adjust_df_materials(modified_df, material_payload):
    df_pickle_path = os.path.join(settings.PROJECT_DATA_DIR, 'cost_df_pickle')
    df_copy = copy.deepcopy(modified_df)

    modified_df = modify_cost(material_payload, df_copy)
    # adjusted_df.to_pickle(df_pickle_path)
    # adjusted_df = pd.read_pickle(df_pickle_path)
    # pandas_class.save_df(adjusted_df, 'df')
    modified_df = calculate_cost_pandas2(modified_df)

    return {
        'adjusted_df': modified_df,
        'adjusted_materials': {
            'silicon': int(modified_df.loc[3, 'silicon']),
            'cu': int(modified_df.loc[3, 'cu']),
            'alu': int(modified_df.loc[3, 'alu']),
            'steel': int(modified_df.loc[3, 'steel']),
            'dicast': int(modified_df.loc[3, 'dicast']),
        }
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
    df['material_other'] = 0.1 * (df['قيمت بلبرينگ'] + df['material_main'])
    df['material_total'] = df['material_other'] + df['قيمت بلبرينگ'] + df['material_main']
    df['cost_overhead'] = df['نرخ سربار'] * df['زمان/ماشين']
    df['cost_wage'] = df['نرخ دستمزد'] * df['زمان /دستمزد']
    df['practical_cost'] = df['material_total'] + df['cost_overhead'] + df['cost_wage']
    df['cost_general'] = 0.5 * df['cost_wage']
    df['cost_calc'] = df['practical_cost'] + df['cost_general'] + df['هزینه بسته بندی']

    return df


def calculate_cost_pandas2(df):
    df['material_main'] = df['وزن سيليكون استيل'] * df['silicon'] + df['سيم لاكي'] * df['cu'] + df['شمش الومينيوم'] * \
                          df['alu'] + df['وزن قطعات چدني (كامل )'] * df['dicast'] + df['ميلگرد فولادي'] * df['steel']
    df['material_other'] = 0.12 * (df['قيمت بلبرينگ'] + df['material_main'])
    df['material_total'] = df['material_other'] + df['قيمت بلبرينگ'] + df['material_main']
    df['cost_overhead'] = df['نرخ سربار'] * df['زمان/ماشين']
    df['cost_wage'] = df['نرخ دستمزد'] * df['زمان /دستمزد']
    df['practical_cost'] = df['material_total'] + df['cost_overhead'] + df['cost_wage']
    df['cost_general'] = 0.9 * df['cost_wage']
    df['cost_calc'] = df['practical_cost'] + df['cost_general'] + df['هزینه بسته بندی']

    return df


def split_specs_if_profit_exists(specs):
    specs_has_profit = list()
    specs_no_profit = list()
    for spec in specs:
        if spec['profit']:
            specs_has_profit.append(spec)
        else:
            specs_no_profit.append(specs_no_profit)
    return {
        'specs_has_profit': specs_has_profit,
        'specs_no_profit': specs_no_profit,
    }


def calculate_cost_of_proforma_by_specs(df, specs):
    specs_splitted = split_specs_routine_and_not_routine(specs)
    cost = 0
    for spec in specs_splitted['routine_specs']:
        cost += calculate_cost_of_spec(df, **spec)
    return cost


def calculate_cost_of_spec(df, **kwargs):
    power = kwargs.get('power', None)
    if type(power) == float:
        power = round(power) if power.is_integer() else power
    rpm = kwargs.get('rpm', None)
    voltage = kwargs.get('voltage', None)
    if voltage > 400:
        return None
    costs = df.loc[:, ['title', 'cost_calc']]
    filt = costs['title'] == f'{power}KW-{rpm}'
    cost_series = costs[filt]
    if not len(cost_series):
        return None
    cost = cost_series['cost_calc'].values[0]
    if voltage == 400:
        cost = 1.1 * cost
    return cost


def get_filename_base_on_date(date):
    date = int(date)
    cost_file_path = os.path.join(settings.PROJECT_DATA_DIR, 'costs')
    files = os.listdir(cost_file_path)
    files_no_ext = [file.split('.')[0] for file in files]
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
    df['قيمت بلبرينگ'] = df['قيمت بلبرينگ'].fillna(0)

    col_names = {
        'POWER(KW)': 'title',
        'قيمت ورق سيليكون استيل': 'silicon',
        'قيمت سيم لاكي': 'cu',
        'قيمت شمش الومينيوم': 'alu',
        ' قيمت قطعات چدني (كامل )': 'dicast',
        'قيمت ميلگرد فولادي': 'steel'
    }
    df.rename(columns=col_names, inplace=True)
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
    df['قيمت بلبرينگ'] = df['قيمت بلبرينگ'].fillna(0)

    col_names = {
        'POWER(KW)': 'title',
        'قيمت ورق سيليكون استيل': 'silicon',
        'قيمت سيم لاكي': 'cu',
        'قيمت شمش الومينيوم': 'alu',
        ' قيمت قطعات چدني (كامل )': 'dicast',
        'قيمت ميلگرد فولادي': 'steel'
    }
    df.rename(columns=col_names, inplace=True)
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
    year = int(file_name[0:4])
    month = int(file_name[4:6])
    day = int(file_name[6:8])
    date = datetime.date(year=year, month=month, day=day)
    return date
