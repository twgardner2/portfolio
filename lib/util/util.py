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
    '''Create a series of the 1st of each month between the start and end 
    dates'''

    # If starts on 1st, use start date
    if start.day == 1:
        first_date = start
    # Else, use 1st of next month
    else:
        tmp = datetime.date(year=start.year, month=start.month, day=1)
        first_date = tmp + relativedelta(months=1)

    # If ends on 1st, use end date
    if end.day == 1:

        last_date = end
    # Else, use 1st of its month
    else:
        last_date = datetime.date(year=end.year, month=end.month, day=1)
    date = first_date
    date_range = [first_date]

    while date < last_date:
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

def previous_first_of_month(date = datetime.date.today()):
    if date.day == 1:
        return_date = date
    else:
        return_date = datetime.date(year=date.year, month=date.month, day=1)
    return(return_date)

def next_first_of_month(date = datetime.date.today()):
    if date.day == 1:
        return_date = date
    else:
        return_date = datetime.date(year=date.year, month=date.month, day=1) + relativedelta(months=1)
    return(return_date)

