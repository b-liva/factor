import os
import datetime
import pandas as pd
import xlrd

from django.conf import settings
from django.test import Client, TestCase
from request.helpers import helpers


class TestUtils(TestCase):
    def setUp(self):
        self.spec = {'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 1000000000}
        self.specs = [
            {'power': 132.0, 'rpm': 1500, 'voltage': 380, 'price': 1000000000},
            {'power': 75, 'rpm': 750, 'voltage': 380, 'price': 180000000},
            {'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 160000000},
            {'power': 2500, 'rpm': 1000, 'voltage': 380, 'price': 20000000000},
            {'power': 160, 'rpm': 1000, 'voltage': 1000, 'price': 7500000000},
        ]
        self.routine_specs = [
            {'power': 132.0, 'rpm': 1500, 'voltage': 380, 'price': 1000000000},
            {'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 160000000},
        ]
        self.not_routine_specs = [
            {'power': 75, 'rpm': 750, 'voltage': 380, 'price': 180000000},
            {'power': 2500, 'rpm': 1000, 'voltage': 380, 'price': 20000000000},
            {'power': 160, 'rpm': 1000, 'voltage': 1000, 'price': 7500000000},
        ]

    def test_return_file_name_based_on_date(self):
        date_str = "20201014"
        filename = helpers.get_filename_base_on_date(date_str)
        self.assertEqual(filename, "20201002")

    def test_selects_file_based_on_filename(self):
        filename = '20200609'
        cost_df = helpers.get_cost_dataframe_by_date_str(filename)
        modified_df = helpers.modify_data_frame(cost_df)
        self.assertEqual(modified_df.iloc[0, 34], 104703578)

    def test_select_routine_specs(self):
        specs_splitted = helpers.split_specs_routine_and_not_routine(self.specs)
        self.assertEqual(len(specs_splitted['routine_specs']), 2)
        self.assertListEqual(self.routine_specs, specs_splitted['routine_specs'])
        self.assertListEqual(self.not_routine_specs, specs_splitted['not_routine_specs'])

    def test_handle_spec_not_in_routine_costs(self):
        date = '20201014'
        self.spec['power'] = 2000
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        self.assertEqual(cost, None)

    def test_calculate_cost_of_proforma_spec(self):
        date = '20201014'
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        self.assertEqual(cost, 879466988)

    def test_calculate_profit_of_proforma_spec(self):
        date = '20201014'
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        profit = self.spec['price'] - cost
        self.assertEqual(round(profit, 2), 120533012)

    def test_add_profit_to_specs(self):
        date = '20201014'
        discount = {
            'lte__90': 0,
            'gt__90': 10,
        }
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, self.specs, discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)
        self.assertEqual(len(specs_profit_split['specs_has_profit']), 2)
        self.assertEqual(len(specs_profit_split['specs_no_profit']), 3)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['price'], 2), 900000000)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['profit'], 2), 20533012.00)
        self.assertEqual(round(specs_profit_split['specs_has_profit'][0]['percent'], 2), 2.33)

    def test_calculate_proforma_profit(self):
        date = '20201014'
        discount = {
            'lte__90': 15,
            'gt__90': 10,
        }

        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, self.specs, discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)

        results = helpers.calculate_profit_of_proforma(specs_profit_split['specs_has_profit'])
        self.assertEqual(round(results['profit'], 2),  26718036.8)
        self.assertEqual(round(results['percent'], 2), 2.65)

    def test_calculate_proforma_profit_one_spec(self):
        date = '20201014'
        discount = {
            'lte__90': 15,
            'gt__90': 10,
        }

        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        specs_profit = helpers.add_profit_to_specs(modified_df, [self.spec], discount_dict=discount)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)

        results = helpers.calculate_profit_of_proforma(specs_profit_split['specs_has_profit'])
        self.assertEqual(round(results['profit'], 2),  20533012.0)
        self.assertEqual(round(results['percent'], 2), 2.33)

    def test_specs_have_no_cost(self):
        date = '20201014'
        discount = {
            'lte__90': 15,
            'gt__90': 10,
        }

        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
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
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)

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
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)

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
        modified_df = helpers.prepare_data_frame_based_on_proforma_date(date)
        cost = helpers.calculate_cost_of_spec(modified_df, **self.spec)
        profit = helpers.calculate_spec_profit_with_discount(cost, self.spec, discount_dict=discount)
        self.assertEqual(profit['profit'], 20533012)
