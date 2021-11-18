from lib.config.config import *
import datetime
# from lib.api.construct_price_history import construct_price_history
import lib.util.util as util
from pprint import pprint
from lib.classes.Inv_Account import Inv_Account
from lib.classes.Bank_Account import Bank_Account
import pandas as pd
import numpy as np

import timeit


# Helper Variables and Functions ########################################################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)
today = datetime.date.today()
end_date = util.previous_first_of_month()

date_range = util.date_range_generator(start_date, end_date)


# Read data ####################################################################
transactions = util.read_timeseries_csv('./data/transactions.csv')
prices = util.read_timeseries_csv('./data/prices.csv')
positions = transactions["symbol"].unique()
accounts = transactions["account"].unique()
categories = set([x[1]['category'] for x in accounts_config.items()])


# Create accounts ##############################################################

## Blacklist accounts for troubleshooting ###
account_blacklist = ['brokerage', 't_ira', 'j_ira', 'trey_529', 'louisa_529']
# account_blacklist = ['brokerage', 'j_ira']
if 'account_blacklist' in locals():
    accounts = np.setdiff1d(accounts, account_blacklist)

print(f'accounts: {transactions["account"].unique()}')
# if 'account_blacklist' in locals():
#     print(f'account_blacklist: {account_blacklist}')
# else:
#     print('No account blacklist')
    
print(f'accounts_final: {accounts}')

## Create Accounts
all_accounts = {}

for account in accounts:
    category = accounts_config.get(account).get('category')
    all_accounts[account] = Inv_Account(account, transactions, prices, date_range, category)

total_value_df = pd.DataFrame(index=date_range)
for category in categories:
    tmp_df = pd.DataFrame(index=date_range)
    # print([x[0] for x in all_accounts.items() if x[1].category==category])
    for account in [x[0] for x in all_accounts.items() if x[1].category==category]:
        tmp_df = tmp_df.join(all_accounts[account].calculate_account_values().iloc[:,-1])
        total_value_df[f'{category}'] = tmp_df.sum(axis=1)

print(total_value_df)
print(total_value_df.index.get_loc(pd.to_datetime(datetime.date(2016,6,13)), method='backfill'))
print('===================')
print(total_value_df.iloc[total_value_df.index.get_loc(pd.to_datetime(datetime.date(2016,6,23)), method='nearest')]['bank'])
# print(total_value_df.iloc[datetime.date(2016,6,23)])

# print(total_value_df)

# Create Plots #################################################################

# from lib.plotting.mpl_plotting import make_matplotlib_plots
# make_matplotlib_plots(all_accounts)

from lib.plotting.plotly_plotting import make_plotly_plots
make_plotly_plots(all_accounts, total_value_df)

# Output CSVs ##################################################################
# for account in accounts:
#     all_accounts[account].calculate_account_values().to_csv(f'./output/{account}_529_values.csv')
