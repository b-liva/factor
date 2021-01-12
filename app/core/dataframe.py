import os
import copy
import pandas as pd
from django.conf import settings


class DataFrame:

    @classmethod
    def get_date_str(cls, date_greg):
        return str(date_greg).replace('-', '')

    @classmethod
    def prepare_data_frame_based_on_proforma_date(cls, date):
        file_name = cls.get_filename_base_on_date(date)
        cost_df = cls.get_cost_dataframe_by_date_str(file_name)
        modified_db = cls.modify_data_frame(cost_df)
        return modified_db, file_name

    @classmethod
    def get_filename_base_on_date(cls, date):
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

    @classmethod
    def get_cost_dataframe_by_date_str(cls, filename):
        cost_file_path = os.path.join(settings.PROJECT_DATA_DIR, f'costs/{filename}.xlsx')
        df_temp = pd.read_excel(cost_file_path)
        return df_temp

    @classmethod
    def modify_data_frame(cls, df):
        if df.iloc[0, 0] == 1:
            df = cls.prepare_data_frame(df)
        else:
            df = cls.prepare_data_frame2(df)
        return df

    @classmethod
    def prepare_data_frame(cls, df):
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

    @classmethod
    def prepare_data_frame2(cls, df):
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

    @classmethod
    def adjust_df_materials(cls, modified_df, material_payload):
        df_copy = copy.deepcopy(modified_df)

        modified_df = cls.modify_cost(material_payload, df_copy)

        modified_df = cls.calculate_cost_pandas2(modified_df)
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

    @classmethod
    def calculate_cost_pandas(cls, df):
        df['material_main'] = df['وزن سيليكون استيل'] * df['silicon'] + df['سيم لاكي'] * df['cu'] + df[
            'شمش الومينيوم'] * \
                              df['alu'] + df['وزن قطعات چدني (كامل )'] * df['dicast'] + df['ميلگرد فولادي'] * df[
                                  'steel']
        df['material_other'] = 0.1 * (df['bearing_cost'] + df['material_main'])
        df['material_total'] = df['material_other'] + df['bearing_cost'] + df['material_main']
        df['cost_overhead'] = df['نرخ سربار'] * df['زمان/ماشين']
        df['cost_wage'] = df['نرخ دستمزد'] * df['زمان /دستمزد']
        df['practical_cost'] = df['material_total'] + df['cost_overhead'] + df['cost_wage']
        df['cost_general'] = 0.5 * df['cost_wage']
        df['cost_calc'] = df['practical_cost'] + df['cost_general'] + df['هزینه بسته بندی']

        return df

    @classmethod
    def calculate_cost_pandas2(cls, df):
        df['material_main'] = df['وزن سيليكون استيل'] * df['silicon'] + df['سيم لاكي'] * df['cu'] + df[
            'شمش الومينيوم'] * \
                              df['alu'] + df['وزن قطعات چدني (كامل )'] * df['dicast'] + df['ميلگرد فولادي'] * df[
                                  'steel']
        df['material_other'] = 0.12 * (df['bearing_cost'] + df['material_main'])
        df['material_total'] = df['material_other'] + df['bearing_cost'] + df['material_main']
        df['cost_overhead'] = df['نرخ سربار'] * df['زمان/ماشين']
        df['cost_wage'] = df['نرخ دستمزد'] * df['زمان /دستمزد']
        df['practical_cost'] = df['material_total'] + df['cost_overhead'] + df['cost_wage']
        df['cost_general'] = 0.9 * df['cost_wage']
        df['cost_calc'] = df['practical_cost'] + df['cost_general'] + df['هزینه بسته بندی']

        return df

    @classmethod
    def modify_cost(cls, payload, df):
        df['silicon'] = payload['silicon']
        df['alu'] = payload['alu']
        df['steel'] = payload['steel']
        df['dicast'] = payload['dicast']
        df['cu'] = payload['cu']
        return df

    @classmethod
    def get_materials_cost(cls, df):
        costs_in_file = {
            'silicon': float(df.loc[3, 'silicon']),
            'cu': float(df.loc[3, 'cu']),
            'alu': float(df.loc[3, 'alu']),
            'steel': float(df.loc[3, 'steel']),
            'dicast': float(df.loc[3, 'dicast']),
        }
        return costs_in_file

    @classmethod
    def get_materials_post_payload(cls, request):
        # todo: remvoe me
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
