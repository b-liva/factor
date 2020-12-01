import datetime
import os
import requests
from django.conf import settings
import pandas as pd
from itertools import groupby

from django.contrib import messages
from django.shortcuts import redirect

from pricedb.models import MotorDB


def print_cost_kw_rpm(costs):
    for cost in costs:
        print(cost['kw'], cost['rpm'], type(cost['rpm']))


def print_cost_title(costs):
    for cost in costs:
        print(cost['title'])


def print_cost(costs):
    # prints items
    print(f"There is {len(costs)} items.")
    for cost in costs:
        print(cost)


def rpm_kw_combinations(costs):
    rpms = [3000, 1500, 1000]
    all_combinations = list()
    for cost in costs:
        for rpm in rpms:
            comb_title = f"{cost['kw_raw']}KW-{rpm}"
            if comb_title not in all_combinations:
                all_combinations.append(comb_title)
    return all_combinations


def fill_blank_costs(all_combinations, costs):
    for combination in all_combinations:
        is_in_list = False
        for cost in costs:
            if combination in cost['title']:
                is_in_list = True

        if not is_in_list:
            [kw, rpm] = combination.split('KW-')
            costs.append({
                'kw': float(kw),
                'rpm': int(rpm),
                'title': combination,
                'base': "---",
                'base_profit': "---",
                'sales': "---",
                'sales_profit': "---",
                'base_file': "---",
                'sale_file': "---",
            })
    return costs


def sort_costs_by(costs, sort_by='kw'):
    return sorted(costs, key=lambda i: (i[sort_by], -i['rpm']))


def group_costs_by(costs, group_by='kw'):
    return groupby(costs, key=lambda i: i[group_by])


def sorted_cost_dict(cost_grp):
    sorted_costs_dict = dict()
    for key, group in cost_grp:
        sorted_costs_dict[key] = list()
        for i in group:
            sorted_costs_dict[key].append(i)
    return sorted_costs_dict


def calculate_profits(costs, df):
    for cost in costs:
        cost_item = cost['title'].split('KW-')
        kw = cost_item[0]
        rpm = cost_item[1]
        cost['kw_raw'] = kw
        cost['kw'] = float(kw)
        cost['rpm'] = int(rpm)
        motor_queryset = MotorDB.objects.filter(motor__kw=kw, motor__speed=rpm, motor__voltage=380)

        if motor_queryset.count():
            motor = motor_queryset[0]
            cost['base'] = motor.base_price
            cost['base_profit'] = (motor.base_price / cost['cost_calc'] - 1) * 100
            cost['sales'] = motor.sale_price
            cost['sales_profit'] = (motor.sale_price / cost['cost_calc'] - 1) * 100

        else:
            cost['base'] = "---"
            cost['sales'] = "---"

        filt = (df['kw'] == cost['kw']) & (df['rpm'] == cost['rpm'])
        base_file = df[filt].loc[:, 'base']
        sale_file = df[filt].loc[:, 'sale']
        if len(base_file) > 0:
            cost['base_file'] = base_file
            cost['sale_file'] = sale_file
        else:
            cost['base_file'] = "---"
            cost['sale_file'] = "---"
    return costs


def price_df():
    data_path = settings.DATA_DIR + 'prices.xlsx'
    df = pd.read_excel(data_path)
    columns = {
        'کیلووات': "kw",
        'دور': 'rpm',
        'کدکالا': 'code',
        'پایه شهریور99': 'base',
        'فروش شهریور99': 'sale'
    }
    df.rename(columns=columns, inplace=True)
    return df


def get_last_costs(request):

    today = datetime.datetime.today()
    host = os.environ.get('CAPIHOST')
    payload = {
        'date': 10000 * today.year + 100 * today.month + today.day,
    }
    headers = {
        'Content-type': 'application/json'
    }

    if request.method == 'POST':
        material_names = ['silicon', 'cu', 'alu', 'steel', 'dicast']
        for material_name in material_names:
            payload[material_name] = int(request.POST.get(material_name).replace(',', ''))
        print(payload)

    try:
        api_req = requests.post(f'http://{host}/get_last_cost', json=payload, headers=headers)
    except:
        messages.add_message(request, level=20, message='خطا')
        return redirect('errorpage')

    costs = api_req.json()['costs']
    materials = api_req.json()['materials']
    return [costs, materials]
