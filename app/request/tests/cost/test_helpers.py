import os
import datetime

import jdatetime
import pandas as pd
import xlrd

from django.conf import settings
from django.test import Client, TestCase
from request.helpers import helpers
from request.models import PrefSpec, Xpref
from request.tests.factory import factories
from request.tests.factory.base_proformas import BaseProformaFactories


class TestUtils(TestCase):
    def setUp(self):
        self.spec = {'qty': 2, 'code': 2, 'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 1000000000}
        self.specs = [
            {'qty': 2, 'code': 2, 'power': 132.0, 'rpm': 1500, 'voltage': 380, 'price': 1000000000},
            {'qty': 2, 'code': 2, 'power': 75, 'rpm': 750, 'voltage': 380, 'price': 180000000},
            {'qty': 2, 'code': 2, 'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 160000000},
            {'qty': 2, 'code': 2, 'power': 2500, 'rpm': 1000, 'voltage': 380, 'price': 20000000000},
            {'qty': 2, 'code': 2, 'power': 160, 'rpm': 1000, 'voltage': 1000, 'price': 7500000000},
        ]
        self.routine_specs = [
            {'qty': 2, 'code': 2, 'power': 132.0, 'rpm': 1500, 'voltage': 380, 'price': 1000000000},
            {'qty': 2, 'code': 2, 'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 160000000},
        ]
        self.not_routine_specs = [
            {'qty': 2, 'code': 2, 'power': 75, 'rpm': 750, 'voltage': 380, 'price': 180000000},
            {'qty': 2, 'code': 2, 'power': 2500, 'rpm': 1000, 'voltage': 380, 'price': 20000000000},
            {'qty': 2, 'code': 2, 'power': 160, 'rpm': 1000, 'voltage': 1000, 'price': 7500000000},
        ]

    def test_return_file_name_based_on_date_str(self):
        date_str = "20201014"
        filename = helpers.get_filename_base_on_date(date_str)
        self.assertEqual(filename, "20201002")

    def test_return_cost_file_date_from_proforma_date(self):
        import jdatetime
        date = jdatetime.date(year=1399, month=7, day=15)
        date = date.togregorian()
        date = helpers.get_date_str(date)
        file_name = helpers.get_filename_base_on_date(date)
        self.assertEqual(file_name, "20201002")

    def test_selects_file_based_on_filename(self):
        filename = '20200609'
        cost_df = helpers.get_cost_dataframe_by_date_str(filename)
        modified_df = helpers.modify_data_frame(cost_df)
        self.assertEqual(modified_df.iloc[0, 34], 104703578)

    def test_get_cost_date_fa_from_file_name(self):
        file_name = "20201002"
        import jdatetime
        date_fa = jdatetime.date(year=1399, month=7, day=11)
        cost_date_fa = helpers.get_date_fa_from_file_name(file_name)
        self.assertEqual(cost_date_fa.year, date_fa.year)
        self.assertEqual(cost_date_fa.month, date_fa.month)
        self.assertEqual(cost_date_fa.day, date_fa.day)

    def test_get_date_from_date_str(self):
        file_name = "20201002"
        date_output = helpers.get_date_from_date_str(file_name)
        date = datetime.date(year=2020, month=10, day=2)
        self.assertEqual(date_output, date)

    def test_split_specs_routine(self):
        specs_splitted = helpers.split_specs_routine_and_not_routine(self.specs)
        self.assertEqual(len(specs_splitted['routine_specs']), 2)
        self.assertListEqual(self.routine_specs, specs_splitted['routine_specs'])

    def test_split_specs_not_routine(self):
        specs_splitted = helpers.split_specs_routine_and_not_routine(self.specs)
        self.assertEqual(len(specs_splitted['not_routine_specs']), 3)
        self.assertListEqual(self.not_routine_specs, specs_splitted['not_routine_specs'])

    def test_handle_spec_not_in_routine_costs(self):
        date = '20201014'
        self.spec['power'] = 2000
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        self.assertEqual(cost, None)

    def test_spec_if_proforma_exist(self):
        discount = {
            'lte__90': 10,
            'gt__90': 10,
        }
        date = '20201014'
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, self.specs, discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)
        self.assertEqual(len(specs_profit_split['specs_no_profit']), 3)
        self.assertEqual(specs_profit_split['specs_no_profit'][0]['power'], self.not_routine_specs[0]['power'])

    def test_calculate_cost_of_proforma_spec(self):
        date = '20201014'
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        self.assertEqual(cost, 879466988)

    def test_calculate_cost_of_proforma_spec_400v(self):
        date = '20201014'
        self.spec['voltage'] = 400
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        self.assertEqual(round(cost, 2), 967413686.8)

    def test_calculate_profit_of_proforma_spec(self):
        date = '20201014'
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        profit = self.spec['price'] - cost
        self.assertEqual(round(profit, 2), 120533012)

    def test_add_profit_to_specs(self):
        date = '20201014'
        discount = {
            'lte__90': 0,
            'gt__90': 10,
        }
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, self.specs, discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)
        self.assertEqual(len(specs_profit_split['specs_has_profit']), 2)
        self.assertEqual(len(specs_profit_split['specs_no_profit']), 3)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['price'], 2), 900000000)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['profit'], 2), 20533012.00)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['percent'], 2), 2.33)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['total_cost'], 2), 1758933976)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['total_price'], 2), 1800000000)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['total_profit'], 2), 41066024.00)
        self.assertEqual(round(specs_profit_split['specs_no_profit'][0]['price']), self.not_routine_specs[0]['price'])
        self.assertEqual(
            round(specs_profit_split['specs_no_profit'][0]['total_price']),
            self.not_routine_specs[0]['price'] * self.not_routine_specs[0]['qty']
        )

    def test_calculate_proforma_profit_temp(self):
        # todo: probably should be removed.
        date = '20201014'
        discount = {
            'lte__90': 15,
            'gt__90': 10,
        }

        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, self.specs, discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)

        results = helpers.calculate_profit_of_proforma(specs_profit_split['specs_has_profit'])
        self.assertEqual(round(results['cost'], 2), 2018563926.40)
        self.assertEqual(round(results['price'], 2), 2072000000.00)
        self.assertEqual(round(results['profit'], 2), 53436073.60)
        self.assertEqual(round(results['percent'], 2), 2.65)

    def test_calculate_proforma_profit_one_spec(self):
        date = '20201014'
        discount = {
            'lte__90': 15,
            'gt__90': 10,
        }

        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, [self.spec], discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)

        results = helpers.calculate_profit_of_proforma(specs_profit_split['specs_has_profit'])
        self.assertEqual(round(results['cost'], 2),  1758933976.00)
        self.assertEqual(round(results['price'], 2),  1800000000.00)
        self.assertEqual(round(results['profit'], 2), 41066024.00)
        self.assertEqual(round(results['percent'], 2), 2.33)

    def test_specs_have_no_cost(self):
        date = '20201014'
        discount = {
            'lte__90': 15,
            'gt__90': 10,
        }

        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, self.not_routine_specs, discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)

        results = helpers.calculate_profit_of_proforma(specs_profit_split['specs_has_profit'])
        self.assertEqual(results['profit'], 0)
        self.assertIsNone(results['percent'], None)

    def test_calculate_cost_of_proforma(self):
        specs = [
            {'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 1651151},
            {'power': 75, 'rpm': 1500, 'voltage': 380, 'price': 8454185},
            {'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 2155151},
            {'power': 160, 'rpm': 1000, 'voltage': 380, 'price': 15485258},
        ]
        date = '20201014'
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)

        cost = helpers.calculate_cost_of_proforma_by_specs(modified_df, specs)
        self.assertEqual(cost, 2548468142.40)

    def test_adjust_materials(self):
        material_payload = {
            'silicon': 250000,
            'cu': 2100000,
            'alu': 500000,
            'steel': 150000,
            'dicast': 220000,
        }

        date = '20201014'
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)

        response = helpers.adjust_df_materials(modified_df, material_payload)
        adjusted_df = response['adjusted_df']
        adjusted_material_payload = response['adjusted_materials']

        spec_cost = helpers.calculate_cost_of_spec(adjusted_df, **self.spec)
        self.assertEqual(adjusted_material_payload['silicon'], material_payload['silicon'])
        self.assertEqual(spec_cost, 811370988)

    def test_perform_discount(self):
        discount = {
            'lte__90': 10,
            'gt__90': 10,
        }
        date = '20201014'
        self.spec['price'] = 1000000000
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        profit = helpers.calculate_spec_profit_with_discount(cost, self.spec, discount_dict=discount)
        self.assertEqual(profit['profit'], 20533012)

    def test_handle_invalid_discounts(self):
        class Req:
            POST = None

        request = Req()
        request.POST = {
            'un90_disc': "",
            'up90_disc': 0,
        }

        discount = helpers.handle_invalid_discounts(request)
        expected_discount = {
            'lte__90': 0,
            'gt__90': 0,
        }
        self.assertDictEqual(discount, expected_discount)

    def test_get_material_cost_post(self):
        class Req:
            POST = None

        request = Req()
        request.POST = {
            "silicon": 300000,
            "cu": 2100000,
            "alu": 500000,
            "steel": 150000,
            "dicast": 220000,
        }

        materials_cost = helpers.get_materials_post_payload(request)
        expected_material_cost = {
            "silicon": 300000,
            "cu": 2100000,
            "alu": 500000,
            "steel": 150000,
            "dicast": 220000,
        }
        self.assertDictEqual(materials_cost, expected_material_cost)

    def test_get_costs(self):
        # df
        # get costs from df
        date = '20201014'
        modified_df, cost_file_name = helpers.prepare_data_frame_based_on_proforma_date(date)
        materials_cost = helpers.get_materials_cost(modified_df)
        self.assertEqual(materials_cost['silicon'], 330000)
        self.assertEqual(materials_cost['cu'], 2100000)
        self.assertEqual(materials_cost['dicast'], 220000)
        self.assertEqual(materials_cost['steel'], 150000)
        self.assertEqual(materials_cost['alu'], 500000)

    def test_remove_comma_from_string_number(self):
        number = "330,000"
        number_without_comma = helpers.remove_comma_from_number(number)
        self.assertEqual(number_without_comma, 330000)

    def test_remove_comma_from_int(self):
        number = 330000
        number_without_comma = helpers.remove_comma_from_number(number)
        self.assertEqual(number_without_comma, 330000)

    def test_remove_comma_from_float(self):
        number = "330,000.22"
        number_without_comma = helpers.remove_comma_from_number(number)
        self.assertEqual(number_without_comma, 330000.22)

    def test_calculate_proforma_profit(self):
        discount = {
            'lte__90': 0,
            'gt__90': 0,
        }

        date_str = '20201014'
        date = helpers.get_date_from_date_str(date_str)
        date_fa = jdatetime.date.fromgregorian(date=date, locale='fa_IR')

        proforma = factories.ProformaFactory.create(number=153)
        proforma.date_fa = date_fa
        proforma.save()

        factories.ProformaSpecFactory.create(xpref_id=proforma, price=1000000000, kw=132, rpm=1500, qty=1)
        factories.ProformaSpecFactory.create(xpref_id=proforma, price=520000000, kw=90, rpm=1500, qty=2)

        profit = helpers.calculate_proforma_profit(proforma, discount=discount)
        self.assertIn('cost', profit)
        self.assertIn('price', profit)
        self.assertIn('profit', profit)
        self.assertIn('percent', profit)

        self.assertEqual(round(profit['cost'], 2), 1822746808.80)
        self.assertEqual(round(profit['price'], 2), 2040000000.00)
        self.assertEqual(round(profit['profit'], 2), 217253191.20)
        self.assertEqual(round(profit['percent'], 2), 11.92)

    def test_proformas_profit(self):
        PrefSpec.objects.all().delete()
        Xpref.objects.all().delete()

        BaseProformaFactories().base_proformas()

        # proformas = [prof1, prof2, prof3]
        proformas = Xpref.objects.filter(is_active=True)

        results = helpers.proformas_profit(proformas)
        self.assertIn('cost', results)
        self.assertIn('price', results)
        self.assertIn('profit', results)
        self.assertIn('percent', results)

        self.assertEqual(round(results['cost'], 2), 4784590556.00)
        self.assertEqual(round(results['price'], 2), 5400000000.00)
        self.assertEqual(round(results['profit'], 2), 615409444.00)
        self.assertEqual(round(results['percent'], 2), 11.4)
