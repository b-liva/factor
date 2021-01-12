from core.dataframe import DataFrame
from core.date import Date


class Proforma:
    @classmethod
    def get_proforma_profit(cls, specs):
        cost_total = 0
        price_total = 0
        profit_total = 0
        for spec in specs:
            cost_total += spec['cost'] * spec['qty']
            profit_total += spec['profit'] * spec['qty']
            price_total += spec['price'] * spec['qty']
        if cost_total:
            percent = (profit_total / cost_total) * 100
        else:
            percent = None
        response = {
            'cost': cost_total,
            'price': price_total,
            'profit': profit_total,
            'percent': percent
        }
        return response

    @classmethod
    def calculate_proforma_profit(cls, proforma, discount=None):
        date = proforma.date_fa.togregorian()
        date = Date.get_date_str(date_greg=date)
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

        modified_df, cost_file_name = DataFrame.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = ProformaSpec.add_profit_to_specs(modified_df, specs_list, discount_dict=discount)
        specs_profit_split = ProformaSpec.split_specs_if_profit_exists(specs_profit)

        results = Proforma.get_proforma_profit(specs_profit_split['specs_has_profit'])
        return results

    @classmethod
    def proformas_profit(cls, proformas):
        result = {
            "cost": 0,
            "price": 0,
            "profit": 0,
            "percent": 0,
        }

        items = ['cost', 'price', 'profit']

        for proforma in proformas:
            profit = cls.calculate_proforma_profit(proforma)
            for item in items:
                result[item] += profit[item]
        if result['cost']:
            result['percent'] = 100 * (result['price'] / result['cost'] - 1)
        else:
            result['percent'] = None
        return result


class ProformaSpec:
    @classmethod
    def split_specs_if_profit_exists(cls, specs):
        specs_has_profit = list()
        specs_no_profit = list()
        for spec in specs:
            if spec['profit']:
                specs_has_profit.append(spec)
            else:
                specs_no_profit.append(spec)
        return {
            'specs_has_profit': specs_has_profit,
            'specs_no_profit': specs_no_profit,
        }

    @classmethod
    def add_profit_to_specs(cls, df, specs, discount_dict=None):
        specs_with_profit = list()
        for spec in specs:
            cost = cls.calculate_cost_of_spec(df, **spec)
            if cost:

                profit = cls.calculate_spec_profit_with_discount(cost, spec, discount_dict)
                percent = 100 * profit['profit'] / cost
                pr = {
                    'cost': cost,
                    'price': profit['price'],
                    'profit': profit['profit'],
                    'percent': percent,
                    'total_cost': spec['qty'] * cost,
                    'total_price': spec['qty'] * profit['price'],
                    'total_profit': spec['qty'] * profit['profit'],
                }
            else:
                pr = {
                    'cost': None,
                    'price': spec['price'],
                    'profit': None,
                    'percent': None,
                    'total_cost': None,
                    'total_price': spec['price'] * spec['qty'],
                    'total_profit': None,
                }
            spec.update(pr)
            specs_with_profit.append(spec)
        return specs_with_profit

    @classmethod
    def calculate_cost_of_spec(cls, df, **kwargs):
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
        return cost

    @classmethod
    def calculate_spec_profit_with_discount(cls, cost, spec, discount_dict=None):
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
