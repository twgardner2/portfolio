<<<<<<< Updated upstream
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
=======
import datetime
# from lib.api.construct_price_history import construct_price_history
import lib.util.util as util
from pprint import pprint
from lib.classes.Account import Account
import matplotlib.pyplot as plt
import numpy as np

# Environment Variables ########################################################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)

today = datetime.date.today()
# end_date = datetime.date(today.year, today.month + 1, 1)
end_date = datetime.date(today.year, 10, 1)

date_range = util.date_range_generator(start_date, end_date)

# Read data ####################################################################
transactions = util.read_timeseries_csv('./data/transactions.csv')
prices = util.read_timeseries_csv('./data/prices.csv')
positions = transactions["symbol"].unique()
accounts = transactions["account"].unique()


# Create accounts ##############################################################
# Create dict of dfs of account values ####
# all_accounts = {}

# for account in accounts:
#     all_accounts[account] = Account(account, date_range, transactions, prices)

# # Create accounts individually for troubleshooting
# t_ira = Account('t_ira', date_range, transactions, prices)
# j_ira = Account('j_ira', date_range, transactions, prices)
brokerage = Account('brokerage', date_range, transactions, prices)
# trey_529 = Account('trey_529', date_range, transactions, prices)

# # Output parts of Accounts to files for troubleshooting
# all_accounts['tsp_mil'].construct_shares_df().to_csv('output/tsp_mil_shares.csv')
# # pprint(all_accounts)
# all_accounts['brokerage'].calculate_account_values().to_csv('output/brokerage_values.csv')
# all_accounts['brokerage'].construct_shares_df().to_csv('output/brokerage_shares.csv')
brokerage.construct_shares_df().to_csv('output/brokerage_shares.csv')
brokerage.calculate_account_values().to_csv('output/brokerage_values.csv')
# Plot account values ##########################################################

# plt.plot(all_accounts['j_ira'].date_range,
#          all_accounts['j_ira'].calculate_account_values().total_value, '-')
# plt.plot(all_accounts['t_ira'].date_range,
#          all_accounts['t_ira'].calculate_account_values().total_value, '-')
# plt.plot(all_accounts['brokerage'].date_range,
#          all_accounts['brokerage'].calculate_account_values().total_value, '-')
# plt.plot(all_accounts['trey_529'].date_range,
#          all_accounts['trey_529'].calculate_account_values().total_value, '-')
# plt.plot(all_accounts['louisa_529'].date_range,
#          all_accounts['louisa_529'].calculate_account_values().total_value, '-')
# plt.plot(all_accounts['george_529'].date_range,
#          all_accounts['george_529'].calculate_account_values().total_value, '-')
# plt.plot(all_accounts['tsp_mil'].date_range,
#          all_accounts['tsp_mil'].calculate_account_values().total_value, '-')
# plt.xlabel("Feature")

# fig = plt.figure()
# ax = plt.axes()

# x = np.linspace(0, 10, 1000)
# ax.plot(x, np.sin(x)).show()

# plt.plot(index, 'total_value', data=j_ira_values, marker='o', markerfacecolor='blue',
#          markersize=12, color='skyblue', linewidth=4)
# plt('index', 'total_value', data=all_accounts['j_ira'], marker='o', markerfacecolor='blue',
#     markersize=12, color='skyblue', linewidth=4)
# plt.plot(j_ira_values.index, j_ira_values['total_value'], marker='', markerfacecolor='blue',
#          markersize=12, color='skyblue', linewidth=4)
# # plt.show()

plt.ylabel("US Dollars")
plt.savefig('output/values.png')
plt.show()
>>>>>>> Stashed changes
