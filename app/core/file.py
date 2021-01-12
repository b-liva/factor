import os
from django.conf import settings
COST_FILE_BASE_PATH = settings.PROJECT_DATA_DIR


def get_filename_base_on_date(date):
    date = int(date)
    cost_file_path = os.path.join(COST_FILE_BASE_PATH, 'costs')
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


def get_cost_file_path(filename):
    return os.path.join(COST_FILE_BASE_PATH, f'costs/{filename}.xlsx')
