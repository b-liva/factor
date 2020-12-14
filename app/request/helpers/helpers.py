import os
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


def add_profits_to_specs(df, specs):
    specs_with_profit = list()
    for spec in specs:
        cost = calculate_cost_of_spec(df, **spec)
        if cost:
            profit = spec['price'] - cost
            pr = {
                'cost': cost,
                'profit': profit
            }
        else:
            pr = {
                'cost': None,
                'profit': None
            }
        spec.update(pr)
        specs_with_profit.append(spec)
    return specs_with_profit


def add_profit_to_specs(df, specs):
    specs_with_profit = list()
    for spec in specs:
        cost = calculate_cost_of_spec(df, **spec)
        if cost:

            profit = spec['price'] - cost
            pr = {
                'cost': cost,
                'profit': profit
            }
        else:
            pr = {
                'cost': None,
                'profit': None,
            }
        spec.update(pr)
        specs_with_profit.append(spec)
    return specs_with_profit


def calculate_profit_of_proforma(specs):
    cost_total = 0
    profit_total = 0
    for spec in specs:
        cost_total += spec['cost']
        profit_total += spec['profit']

    return {
        'cost': cost_total,
        'profit': profit_total
    }


def prepare_data_frame_based_on_proforma_date(date):
    file_name = get_filename_base_on_date(date)
    cost_df = get_cost_dataframe_by_date_str(file_name)
    modified_db = modify_data_frame(cost_df)
    return modified_db


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
    rpm = kwargs.get('rpm', None)
    voltage = kwargs.get('voltage', None)
    if voltage > 400:
        return None
    costs = df.loc[:, ['title', 'cost']]
    filt = costs['title'] == f'{power}KW-{rpm}'
    cost_series = costs[filt]
    if not len(cost_series):
        return None
    cost = cost_series['cost'].values[0]
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
