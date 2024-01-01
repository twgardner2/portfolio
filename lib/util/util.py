import datetime
from dateutil.relativedelta import relativedelta
import shutil
from os import path
import pandas as pd
import re
import sys


def dateparse(x):
    return (pd.to_datetime(x, format='%Y%m%d'))


def read_timeseries_csv(file, shape):

    data = pd.read_csv(
        file,
        sep=r'\s*,\s*',
        engine='python',
        index_col='date',
        parse_dates=['date'],
        date_parser=dateparse
    )

    # data['date'] = data['date'].dt.date
    data.index = pd.to_datetime(data.index)
    # Validate column types - Iterate over columns
    for (col, colData) in data.items():

        # Set flag to check that each column has a match in the validation object
        columnMatchFound = False

        # Iterate over validation object
        for key in shape:

            # If match is found
            if re.search(key, col):

                # Set flag
                columnMatchFound = True

                # Try assertion
                try:
                    col_matches_allowed_dts = [
                        dtype(colData) for dtype in shape[key]]
                    assert any(col_matches_allowed_dts) or data[col].isnull(
                    ).all(), "Input validation error"
                    break
                except AssertionError as error:
                    print(f'{error} in {file}')
                    allowed_dtypes = [dtype.__name__ for dtype in shape[key]]
                    print(
                        f'   ☹  {col} should pass one of {allowed_dtypes} but is {data[col].dtype}')
                    sys.exit(1)

        # If flag never set, error
        if not columnMatchFound:
            print(
                f'   ☹  No match found for column "{col}" of {file} in validation shape definition')
            sys.exit(1)

    return (data)


def validate_inputs(transactions, prices, bank_balances, home_equity):
    validation_errors = []

    # Validate price data
    # Price allowed to be blank if "inactive." A -1 indicates a column is
    # inactive and allowed to be validly left blank. A float turns the column
    # back active and disallows further blanks until another -1 is present.
    for df in [prices, bank_balances]:
        for (col, colData) in df.items():
            position_active = False
            for index, el in colData.items():

                if pd.isna(el) and position_active:
                    validation_errors.append(
                        f'☹  {col} is missing a price on {index.date()}')
                    # print(f'☹ {col} is missing a price on {index.date()}')
                    # print(f"{index}: {el}")
                    # print(f"{index.date()}: {el}")
                elif el == -1:
                    position_active = False
                elif not pd.isna(el) and el != -1:
                    position_active = True
    # for (col, colData) in prices.iteritems():
    #     position_active = False
    #     for index, el in colData.iteritems():

    #         if pd.isna(el) and position_active:
    #             validation_errors.append(f'☹  {col} is missing a price on {index.date()}')
    #             # print(f'☹ {col} is missing a price on {index.date()}')
    #             # print(f"{index}: {el}")
    #             # print(f"{index.date()}: {el}")
    #         elif el==-1:
    #             position_active = False
    #         elif not pd.isna(el) and el!=-1:
    #             position_active = True

    # Validate bank data
    # Price allowed to be blank if "inactive." A -1 indicates a column is
    # inactive and allowed to be validly left blank. A float turns the column
    # back active and disallows further blanks until another -1 is present.

    # Check that there are prices for all months in which there are shares for each position

    # Check validation_errors: if len > 0, print errors and exit w/ code 1
    if len(validation_errors) > 0:
        for error in validation_errors:
            print(error)
        sys.exit(1)

    return True


def date_range_generator(start, end):
    '''Create a series of the 1st of each month between the start and end 
    dates'''

    # Make sure start and end are of type datetime.date

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
        # print(f'')
    # Else, use 1st of its month
    else:
        last_date = datetime.date(year=end.year, month=end.month, day=1)

    date = first_date
    date_range = [first_date]

    # print(f'   {date} - type(date): {type(date)}')
    # print(f'   {last_date} - type(last_date): {type(last_date)}')
    if isinstance(date, pd.Timestamp):
        # print("its a timestamp")
        date = date.date()
    while date < last_date:
        date = date + relativedelta(months=1)
        # print(f'type(date): {type(date)}')
        date_range.append(date)
    # print('-------')

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


def previous_first_of_month(date=datetime.date.today()):
    if date == datetime.date.today() and date.day == 1:
        return_date = date
    elif date.day == 1:
        return_date = date + relativedelta(months=-1)
    else:
        return_date = datetime.date(year=date.year, month=date.month, day=1)

    if not isinstance(return_date, datetime.date):
        print(f'>>>not a date')
        return_date = return_date.date()
    return (return_date)


def next_first_of_month(date=datetime.date.today()):
    if date.day == 1:
        return_date = date
    else:
        return_date = datetime.date(
            year=date.year, month=date.month, day=1) + relativedelta(months=1)
    return (return_date)
