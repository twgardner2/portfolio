import datetime
# from lib.api.construct_price_history import construct_price_history
import lib.util.util as util
from pprint import pprint
from lib.classes.Account import Account
import matplotlib.pyplot as plt
import numpy as np

import timeit

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

## Blacklist accounts for troubleshooting ###
account_blacklist = ['brokerage', 't_ira']
accounts = np.setdiff1d(accounts, account_blacklist)

print(f'accounts: {transactions["account"].unique()}')
print(f'account_blacklist: {account_blacklist}')
print(f'accounts_final: {accounts}')

## Create dict of dfs of account values ####
all_accounts = {}

for account in accounts:
    all_accounts[account] = Account(account, date_range, transactions, prices)

# # Create accounts individually for troubleshooting
# t_ira = Account('t_ira', date_range, transactions, prices)
# j_ira = Account('j_ira', date_range, transactions, prices)
# brokerage = Account('brokerage', date_range, transactions, prices)
# thrivent = Account('thrivent', date_range, transactions, prices)

# Plot account values ##########################################################

plt.plot(all_accounts['j_ira'].date_range,
         all_accounts['j_ira'].calculate_account_values().total_value, '-')
plt.plot(all_accounts['t_ira'].date_range,
         all_accounts['t_ira'].calculate_account_values().total_value, '-')
plt.plot(all_accounts['brokerage'].date_range,
         all_accounts['brokerage'].calculate_account_values().total_value, '-')
plt.plot(all_accounts['trey_529'].date_range,
         all_accounts['trey_529'].calculate_account_values().total_value, '-')
plt.plot(all_accounts['louisa_529'].date_range,
         all_accounts['louisa_529'].calculate_account_values().total_value, '-')
plt.plot(all_accounts['george_529'].date_range,
         all_accounts['george_529'].calculate_account_values().total_value, '-')
plt.plot(all_accounts['tsp_mil'].date_range,
         all_accounts['tsp_mil'].calculate_account_values().total_value, '-')
# plt.plot(thrivent.date_range,
#          thrivent.calculate_account_values().total_value, '-')
# plt.plot(brokerage.date_range,
#          brokerage.calculate_account_values().total_value, '-')
# plt.plot(metron_401k.date_range,
#          metron_401k.calculate_account_values().total_value, '-')
# plt.xlabel("Feature")


# plt.plot(index, 'total_value', data=j_ira_values, marker='o', markerfacecolor='blue',
#          markersize=12, color='skyblue', linewidth=4)
# plt('index', 'total_value', data=all_accounts['j_ira'], marker='o', markerfacecolor='blue',
#     markersize=12, color='skyblue', linewidth=4)
# plt.plot(j_ira_values.index, j_ira_values['total_value'], marker='', markerfacecolor='blue',
#          markersize=12, color='skyblue', linewidth=4)
# plt.show()

plt.ylabel("US Dollars")
plt.savefig('output/values.png')
plt.show()
