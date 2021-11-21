from lib.config.config import *
import datetime
# from lib.api.construct_price_history import construct_price_history
import lib.util.util as util
from pprint import pprint
from lib.classes.Inv_Account import Inv_Account
from lib.classes.Bank_Account import Bank_Account
from lib.classes.Home_Equity import Home_Equity
import pandas as pd
import numpy as np
import warnings

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
bank_balances = util.read_timeseries_csv('./data/bank.csv')
home_equity = util.read_timeseries_csv('./data/home_equity.csv')

# Get relevant values from raw data
inv_accounts = transactions['account'].unique()
bank_accounts = bank_balances['account'].unique()
homes = home_equity['home'].unique()
categories = set([x[1]['category'] for x in accounts_config.items()])

# Create Bank Accounts #########################################################

# wells_fargo = Bank_Account('wells_fargo_checking', bank_balances, date_range, accounts_config.get('wells_fargo_checking').get('category'))
# print(wells_fargo.calculate_account_values())

# Create accounts ##############################################################
'''Going to make accounts from the accounts_config object, but will check 
against all of the accounts in the raw data and throw a warning if there is an
account missing in the config'''

### Warn if any account name is in raw data but not the config
accounts_in_config = np.array(list(accounts_config.keys()))
accounts_in_raw_data = np.concatenate((inv_accounts, bank_accounts, homes))
accounts_in_raw_data_but_not_config = \
    np.setdiff1d(accounts_in_raw_data, accounts_in_config)
if len(accounts_in_raw_data_but_not_config):
    warnings.warn(
        f'''WARNING: The following accounts are in the raw data but are not in 
        accounts_config and will be ignored: 
        {accounts_in_raw_data_but_not_config}''')

## Blacklist accounts for troubleshooting ###
account_blacklist = ['brokerage', 't_ira', 'j_ira', 'trey_529', 'louisa_529']
# account_blacklist = ['brokerage', 'j_ira']
if 'account_blacklist' in locals():
    accounts = np.setdiff1d(accounts_in_config, account_blacklist)
else:
    accounts = accounts_in_config

if 'account_blacklist' in locals():
    print(f'account_blacklist: {account_blacklist}')
else:
    print('No account blacklist')
    
print(f'accounts_final: {accounts}')

## Create Accounts
all_accounts = {}

for account in accounts:
    category = accounts_config.get(account).get('category')
    account_class =  accounts_config.get(account).get('class')
    if account_class == 'Inv_Account':
        all_accounts[account] = Inv_Account(account, transactions, prices, category)
    elif account_class == 'Bank_Account':
        all_accounts[account] = Bank_Account(account, bank_balances, category)
    elif account_class == 'Home_Equity':
        all_accounts[account] = Home_Equity(account, home_equity, category)



total_value_df = pd.DataFrame(index=date_range)
for category in categories:
    tmp_df = pd.DataFrame(index=date_range)
    # print([x[0] for x in all_accounts.items() if x[1].category==category])
    for account in [x[0] for x in all_accounts.items() if x[1].category==category]:
        tmp_df = tmp_df.join(all_accounts[account].calculate_account_values().iloc[:,-1])
        total_value_df[f'{category}'] = tmp_df.sum(axis=1)

print(total_value_df)

# Create Plots #################################################################

# from lib.plotting.mpl_plotting import make_matplotlib_plots
# make_matplotlib_plots(all_accounts)

from lib.plotting.plotly_plotting import make_plotly_plots
make_plotly_plots(all_accounts, total_value_df)

# Output CSVs ##################################################################
# for account in accounts:
#     all_accounts[account].calculate_account_values().to_csv(f'./output/{account}_529_values.csv')
