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
