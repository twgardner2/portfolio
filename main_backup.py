# %%
import datetime
from dateutil.relativedelta import relativedelta
import csv
import pandas as pd
import requests
import json
# from lib.api import fetch_price_history
from lib.api.construct_price_history import construct_price_history
import lib.calc.calc as calc
import lib.util.util as util
import matplotlib.pyplot as plt
from pprint import pprint

# %%
# Environment Variables ###########################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)

today = datetime.date.today()
end_date = datetime.date(today.year, today.month + 1, 1)
###################################################

# %%
# Read data #######################################
transactions = util.read_timeseries_csv('./data/transactions.csv')
# print(transactions)

# %%
prices = util.read_timeseries_csv('./data/prices.csv')
# print(prices)

positions = transactions["symbol"].unique()
accounts = transactions["account"].unique()

###################################################
# %%
date_range = util.date_range_generator(start_date, end_date)

# Create dict of dfs of account values ####

all_accounts = {}

for index, account in enumerate(accounts):
    shares = calc.construct_shares_df(date_range, account, transactions)
    values = calc.calculate_account_values(shares, prices)
    all_accounts[account] = values

pprint(all_accounts)
########################################################


# brokerage_shares = calc.construct_shares_df(
#     date_range, "brokerage", transactions)
# # brokerage_shares.to_csv('brokerage_shares.csv')

# j_ira_shares = calc.construct_shares_df(date_range, "j_ira", transactions)
# # j_ira_shares.to_csv('j_ira_shares.csv')

# # t_ira_shares = construct_shares_df(date_range, "t_ira", transactions)
# # t_ira_shares.to_csv('t_ira_shares.csv')

# # brokerage_values = calculate_account_values(brokerage_shares, prices)

# # brokerage_values = calculate_account_values(brokerage_shares, prices)
# # print(brokerage_values)


# j_ira_values = calc.calculate_account_values(j_ira_shares, prices)
# # print(j_ira_values)

# # plt.plot(index, 'total_value', data=j_ira_values, marker='o', markerfacecolor='blue',
# #          markersize=12, color='skyblue', linewidth=4)
# plt.plot(j_ira_values.index, j_ira_values['total_value'], marker='', markerfacecolor='blue',
#          markersize=12, color='skyblue', linewidth=4)
# # plt.show()
# plt.savefig('j_ira.png')
# %%
