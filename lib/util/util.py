import datetime
from dateutil.relativedelta import relativedelta
import shutil
from os import path
import pandas as pd


def dateparse(x):
    return(pd.to_datetime(x, format='%Y%m%d').date())


def read_timeseries_csv(file):
    data = pd.read_csv(
        file,
        sep=r'\s*,\s*',
        engine='python',
        index_col='date',
        parse_dates=['date'],
        date_parser=dateparse
    )
    return(data)


def date_range_generator(start, end):

    date = start
    date_range = [start]

    while date < end:
        date = date + relativedelta(months=1)
        date_range.append(date)

    date_range = pd.to_datetime(date_range)
    return (date_range)


def backup_data_file(fn):

    # Copy file
    if path.exists(f'./data/{fn}'):
        src = path.realpath(f'./data/{fn}')
        print(src)

        src_dirname = path.dirname(src)
        src_basename = path.basename(src)
        src_filename, src_extenstion = src_basename.split('.')

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        print(timestamp)
        dest_dirname = f'{src_dirname}/backup'
        dest_basename = f'{src_filename}_{timestamp}.{src_extenstion}'
        dest = path.realpath(f'{dest_dirname}/{dest_basename}')

        # print(src)
        # dst = src + '.backup'
        shutil.copy(src, dest)


# backup_data_file('prices.csv')
# root, extension = 'this/is/a/file/path/prices.csv'.split('.')
# # print('this/is/a/file/path/prices.csv'.split('.'))
# print(f'root: {root}')
# print(f'extension: {extension}')
