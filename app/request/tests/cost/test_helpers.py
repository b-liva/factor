import os
import datetime
import pandas as pd
import xlrd

from django.conf import settings
from django.test import Client, TestCase
from request.helpers import helpers


class TestUtils(TestCase):
    def setUp(self):
        self.spec = {'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 1055360385.6}
        self.specs = [
            {'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 456007},
            {'power': 75, 'rpm': 750, 'voltage': 380, 'price': 4542467},
            {'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 4598767},
            {'power': 2500, 'rpm': 1000, 'voltage': 380, 'price': 4556767},
            {'power': 160, 'rpm': 1000, 'voltage': 1000, 'price': 4514167},
        ]
        self.routine_specs = [
            {'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 456007},
            {'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 4598767},
        ]
        self.not_routine_specs = [
            {'power': 75, 'rpm': 750, 'voltage': 380, 'price': 4542467},
            {'power': 2500, 'rpm': 1000, 'voltage': 380, 'price': 4556767},
            {'power': 160, 'rpm': 1000, 'voltage': 1000, 'price': 4514167},
        ]

    def test_return_file_name_based_on_date(self):
        date_str = "20201014"
        filename = helpers.get_filename_base_on_date(date_str)
        self.assertEqual(filename, "20201002")

    def test_selects_file_based_on_filename(self):
        filename = '20200609'
        cost_df = helpers.get_cost_dataframe_by_date_str(filename)
        modified_db = helpers.modify_data_frame(cost_df)
        self.assertEqual(modified_db.iloc[0, 34], 104703578)

    def test_select_routine_specs(self):

        specs_splitted = helpers.split_specs_routine_and_not_routine(self.specs)
        self.assertEqual(len(specs_splitted['routine_specs']), 2)
        self.assertListEqual(self.routine_specs, specs_splitted['routine_specs'])
        self.assertListEqual(self.not_routine_specs, specs_splitted['not_routine_specs'])

    def test_handle_spec_not_in_routine_costs(self):
        date = '20201014'
        self.spec['power'] = 2000
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)
        cost = helpers.calculate_cost_of_spec(modified_db, **self.spec)
        self.assertEqual(cost, None)

    def test_calculate_cost_of_proforma_spec(self):
        date = '20201014'
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)
        cost = helpers.calculate_cost_of_spec(modified_db, **self.spec)
        self.assertEqual(cost, 879466988)

    def test_calculate_profit_of_proforma_spec(self):
        date = '20201014'
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)
        cost = helpers.calculate_cost_of_spec(modified_db, **self.spec)
        profit = self.spec['price'] - cost
        self.assertEqual(round(profit, 2), 175893397.6)

    def test_add_profit_to_specs(self):
        date = '20201014'
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)
        specs_profit = helpers.add_profit_to_specs(modified_db, self.specs)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)
        self.assertEqual(len(specs_profit_split['specs_has_profit']), 2)
        self.assertEqual(len(specs_profit_split['specs_no_profit']), 3)

    def test_calculate_proforma_profit(self):
        date = '20201014'
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)
        specs_profit = helpers.add_profit_to_specs(modified_db, self.specs)
        specs_profit_split = helpers.split_specs_if_profit_exists(specs_profit)
        results = helpers.calculate_profit_of_proforma(specs_profit_split['specs_has_profit'])
        self.assertEqual(results['profit'],  -1004227189.2)

    def test_calculate_cost_of_proforma(self):
        specs = [
            {'power': 132, 'rpm': 1500, 'voltage': 380, 'price': 1651151},
            {'power': 75, 'rpm': 1500, 'voltage': 380, 'price': 8454185},
            {'power': 18.5, 'rpm': 3000, 'voltage': 380, 'price': 2155151},
            {'power': 160, 'rpm': 1000, 'voltage': 380, 'price': 15485258},
        ]
        date = '20201014'
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)

        cost = helpers.calculate_cost_of_proforma_by_specs(modified_db, specs)
        self.assertEqual(cost, 2548468142.40)

    def test_calculate_profit_of_specs(self):
        date = '20201014'
        file_name = helpers.get_filename_base_on_date(date)
        cost_df = helpers.get_cost_dataframe_by_date_str(file_name)
        modified_db = helpers.modify_data_frame(cost_df)
        profits = helpers.add_profits_to_specs(modified_db, self.specs)
        self.assertEqual(len(profits), 5)
