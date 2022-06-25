from lib.config.config import *
import datetime
import lib.util.util as util
import pandas as pd
import numpy as np
import warnings
import time
import re

# Custom classes
from lib.classes.Inv_Account import Inv_Account
from lib.classes.Bank_Account import Bank_Account
from lib.classes.Home_Equity import Home_Equity


# Argument Parser
from argparse import ArgumentParser
parser = ArgumentParser(description = 'A portfolio analysis tool')
parser.add_argument('-np', '--no-plot', action='store_true', help='Set this flag to skip plotting')
parser.add_argument('-nv', '--no-validation', action='store_true', help='Set this flag to skip validating inputs')
parser.add_argument('-x', '--exclude', help='Pass a comma-separated list of accounts to exclude')
parser.add_argument('-nc', '--no-csv', action='store_true', help='Set this flag to skip writing out CSVs')
args = parser.parse_args()

# Collect runtime data
runtimes = []
runtimes.append({'label': 'Start','time': time.time()})

# Helper Variables and Functions ###############################################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)
today = datetime.date.today()
end_date = util.previous_first_of_month()
date_range = util.date_range_generator(start_date, end_date)
# Read data ####################################################################
transactions = util.read_timeseries_csv(
    file = './data/transactions.csv', 
    shape = {
        'account':              pd.api.types.is_object_dtype,
        'symbol':               pd.api.types.is_object_dtype,
        'shares':               pd.api.types.is_object_dtype,
        'price':                pd.api.types.is_float_dtype,
        'type':                 pd.api.types.is_object_dtype,
        'note':                 pd.api.types.is_object_dtype,
    }
)

prices = util.read_timeseries_csv(
    file = './data/prices.csv', 
    shape = {
        '.*':                   pd.api.types.is_float_dtype,
    }
)

bank_balances = util.read_timeseries_csv(
    file = './data/bank.csv', 
    shape = {
        '.*':                   pd.api.types.is_float_dtype,
    }
)

home_equity = util.read_timeseries_csv(
    file = './data/home_equity.csv', 
    shape = {
        # 'home':                 pd.api.types.is_object_dtype,
        'market_value':         pd.api.types.is_float_dtype,
        'mortgage_principal':   pd.api.types.is_float_dtype,
        'note':                 pd.api.types.is_object_dtype,
    }
)
runtimes.append({'label': 'Read Data','time': time.time()})

# Validate data ################################################################
if args.no_validation:
    print('Skipping input validation...')
else:
    util.validate_inputs(transactions, prices, bank_balances, home_equity)
    runtimes.append({'label': 'Input Validation', 'time':time.time()})

# Get categorical values from raw data #########################################
inv_accounts = transactions['account'].unique()
bank_accounts = bank_balances.columns.unique()
homes = home_equity.columns.unique().to_list()
homes = [home for home in homes if re.search(r'mortgage_principal_(.*)', home)]
homes = [re.search(r'mortgage_principal_(.*)', x).groups()[0] for x in homes]
categories = set([x[1]['category'] for x in accounts_config.items()])

# Create accounts ##############################################################
'''Make accounts from the accounts_config object, but will check 
against all of the accounts in the raw data and throw a warning if there is an
account missing in the config'''

### Warn if any account name is in raw data but not the config
accounts_in_config = np.array(list(accounts_config.keys()))
accounts_in_raw_data = np.concatenate((inv_accounts, bank_accounts, homes))
accounts_in_raw_data_but_not_config = \
    np.setdiff1d(accounts_in_raw_data, accounts_in_config)
if len(accounts_in_raw_data_but_not_config):
    warnings.warn(
        f'''WARNING: The following accounts are in the raw data but are '''\
        f'''not in accounts_config and will be ignored: ''' \
        f'''{accounts_in_raw_data_but_not_config}''')

## Exclude accounts from analysis
if args.exclude:
    accounts_to_exclude = args.exclude.split(',')
    print(f"Excluding accounts: {accounts_to_exclude}")
    accounts = np.setdiff1d(accounts_in_config, accounts_to_exclude)

    accounts_to_exclude_that_dont_exist = np.setdiff1d(accounts_to_exclude, accounts_in_raw_data)
    if len(accounts_to_exclude_that_dont_exist):
        warnings.warn(
        f'''WARNING: The following accounts passed to be excluded don't ''' \
        f'''exist in accounts_config: {accounts_to_exclude_that_dont_exist}''')
else:
    accounts = accounts_in_config

print(f'Included accounts: {accounts}')

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

runtimes.append({'label': 'Create Accounts','time': time.time()})

total_value_df = pd.DataFrame(index=date_range)
for category in categories:
    tmp_df = pd.DataFrame(index=date_range)
    for account in [x[0] for x in all_accounts.items() if x[1].category==category]:
        tmp_df = tmp_df.join(all_accounts[account].calculate_account_values().iloc[:,-1])
    total_value_df[f'{category}'] = tmp_df.sum(axis=1)

runtimes.append({'label': 'Create Categorized Accounts Data Frame','time': time.time()})

# Create Plots #################################################################
if not args.no_plot:
    from lib.plotting.plotly_plotting import make_plotly_accounts_plot
    from lib.plotting.plotly_plotting import make_plotly_categories_plot
    from lib.plotting.plotly_plotting import make_plotly_single_account_plot

    make_plotly_accounts_plot(all_accounts)
    make_plotly_categories_plot(total_value_df)

    # make_plotly_single_account_plot(all_accounts['j_ira'])
    # make_plotly_single_account_plot(all_accounts['brokerage'])
    # make_plotly_single_account_plot(all_accounts['tsp_civ'])

    runtimes.append({'label': 'Create Plots','time': time.time()})
else:
    print('Skipping plotting...')

# Output CSVs ##################################################################
if not args.no_csv:
    for account in accounts:
        all_accounts[account].calculate_account_values().to_csv(f'./output/csvs/{account}_values.csv')
    runtimes.append({'label': 'Create CSVs','time': time.time()})

# Print runtimes
for i, time in enumerate(runtimes):
    if i>0:
        print(f'Time to {time["label"]}: {time["time"]-runtimes[i-1]["time"]:.2f}')
