import datetime
from dateutil.relativedelta import relativedelta
import csv
import pandas as pd
import requests
import json
from lib.api import fetch_price_history
# from lib.api import construct_price_history
# import lib.api.construct_price_history as construct_price_history
from lib.api.construct_price_history import construct_price_history
# from lib.util import util
import lib.util.util as util

# print(pd.show_versions())

# Environment Variables ###########################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)

today = datetime.date.today()
end_date = datetime.date(today.year, today.month + 1, 1)
###################################################

# print(util.dateparse('19820623'))

# Read data #######################################
transactions = util.read_timeseries_csv('./data/transactions.csv')
# print(transactions)
# print(transactions.index)

prices = util.read_timeseries_csv('./data/prices.csv')
# print(prices)

# positions = transactions["symbol"].unique()
# accounts = transactions["account"].unique()

###################################################

date_range = util.date_range_generator(start_date, end_date)


def calculate_shares(date, account, symbol, transactions):
    symbol_transactions = transactions.query(
        'symbol == @symbol & account == @account & date <= @date')  #
    shares = symbol_transactions['shares'].sum()

    return (shares)


def construct_shares_df(date_range, account, transactions):
    df = pd.DataFrame()
    df['date'] = date_range

    account_transactions = transactions.query('account == @account')
    # print(account_transactions)
    account_symbols = account_transactions['symbol'].unique()
    # print(account_symbols)

    for symbol in account_symbols:
        symbol_shares = []
        for date in date_range:
            shares_amount = calculate_shares(
                date, account, symbol, transactions)
            symbol_shares.append(shares_amount)

        df[symbol] = symbol_shares

    # print(df)
    return(df)


def construct_account_values(shares_df, prices_df):
    # account_symbols = shares_df.columns
    print(shares_df.index)
    print(prices_df.index)
    # df = shares_df.merge(prices_df,
    #                      #  on='date',
    #                      left_index=True,
    #                      right_index=True,
    #                      how='left',
    #                      suffixes=('_shares', '_price'))
    # return(df)


# util.backup_data_file('prices.csv')
# construct_price_history(date_range, positions)
brokerage_shares = construct_shares_df(date_range, "brokerage", transactions)
# brokerage_shares.to_csv('brokerage_shares.csv')

# j_ira_shares = construct_shares_df(date_range, "j_ira", transactions)
# j_ira_shares.to_csv('j_ira_shares.csv')

# t_ira_shares = construct_shares_df(date_range, "t_ira", transactions)
# t_ira_shares.to_csv('t_ira_shares.csv')

# brokerage_values = construct_account_values(brokerage_shares, prices)

df = construct_account_values(brokerage_shares, prices)
print(df)
