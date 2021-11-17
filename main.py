import datetime
# from lib.api.construct_price_history import construct_price_history
import lib.util.util as util
from pprint import pprint
from lib.classes.Account import Account
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import multiprocessing as mp
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.sharedctypes import Array
import ctypes
import timeit

import plotly.graph_objects as go

# Helper Variables and Functions ########################################################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)
today = datetime.date.today()
end_date = util.previous_first_of_month()

date_range = util.date_range_generator(start_date, end_date)

accounts_config = {
    'usaa_savings': {
        'label':'USAA Savings',
        'category': 'bank'
    },
    'usaa_checking': {
        'label':'USAA Checking',
        'category': 'bank'
    },
    'wells_fargo_checking': {
        'label':'Wells Fargo Checking',
        'category': 'bank'
    },
    't_ira': {
        'label':'T IRA',
        'category': 'retirement'
    },
    'j_ira': {
        'label': 'J IRA',
        'category': 'retirement'
    },
    'brokerage': {
        'label': 'Brokerage',
        'category': 'retirement',
    },
    'trey_529': {
        'label': '529 - Trey',
        'category': 'college',
    },
    'louisa_529': {
        'label': '529 - Louisa',
        'category': 'college',
    },
    'george_529': {
        'label': '529 - George',
        'category': 'college',
    },
    'metron_401k': {
        'label': 'Metron 401K',
        'category': 'retirement',
    },
    'thrivent': {
        'label': 'Thrivent',
        'category': 'retirement',
    },
    'tsp_civ': {
        'label': 'TSP - Civilian',
        'category': 'retirement',
    },
    'tsp_mil': {
        'label': 'TSP - Military',
        'category': 'retirement',
    },
}

annotations = [
    {'date': pd.to_datetime('20130531'),
     'text': 'Last Day in Navy',
    },
    {'date': pd.to_datetime('20130731'),
     'text': 'Bought Sienna'
    },
    {'date': pd.to_datetime('20180630'),
     'text': 'Bought Prius'
    },
    {'date': pd.to_datetime('20191016'),
     'text': 'Bought 4903 Chipper Lane'
    },
    {'date': pd.to_datetime('20200501'),
     'text': 'Started at Metron'
    },
    {'date': pd.to_datetime('20150602'),
     'text': 'Started at Summit'
    },
    {'date': pd.to_datetime('20210402'),
     'text': 'Sold 5236 Elston Lane'
    },
]

category_annotations = [
    {'date': pd.to_datetime('20130531'),
     'text': 'Last Day in Navy',
     'point_to': 'bank' 
    },
    {'date': pd.to_datetime('20130731'),
     'text': 'Bought Sienna',
     'point_to': 'retirement'
    },
    {'date': pd.to_datetime('20180630'),
     'text': 'Bought Prius'
    },
    {'date': pd.to_datetime('20191016'),
     'text': 'Bought 4903 Chipper Lane'
    },
    {'date': pd.to_datetime('20200501'),
     'text': 'Started at Metron'
    },
    {'date': pd.to_datetime('20150602'),
     'text': 'Started at Summit'
    },
    {'date': pd.to_datetime('20210402'),
     'text': 'Sold 5236 Elston Lane'
    },
]

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


## Create Accounts across Pool
# def create_account(account, transactions, prices, date_range, category, config):
#     category = config.get(account).get('category')
#     return({account: Account(account, transactions, prices, date_range, category)})
# with SharedMemoryManager() as smm:
#     sh_transactions = mp.Value(ctypes.py_object)
#     sh_prices = mp.Value(ctypes.py_object)
#     # sh_date_range = mp.Array(date_range)
#     # sh_date_range = multiprocessing.sharedctypes.Array(date_range)
#     sh_date_range = mp.Value(date_range)

#     def create_account(account):
#         # sh_transactions, sh_prices, sh_date_range, sh_config
#         # category = sh_config.get(account).get('category')
#         category='bank'
#         return({account: Account(account, sh_transactions, sh_prices, sh_date_range, category)})

#     with mp.Pool() as p:
#         p.map(Account, accounts)



# test_all_accounts = Pool.starmap(create_account, zip(accounts, ))
# print('asdfasdf')
# print(list(zip(accounts, [transactions]*len(accounts))))
# print('asdfasdf')


## Create Accounts
all_accounts = {}

for account in accounts:
    category = accounts_config.get(account).get('category')
    all_accounts[account] = Account(account, transactions, prices, date_range, category)

total_value_df = pd.DataFrame(index=date_range)
for category in categories:
    tmp_df = pd.DataFrame(index=date_range)
    for account in [x[0] for x in all_accounts.items() if x[1].category==category]:
        tmp_df = tmp_df.join(all_accounts[account].calculate_account_values().iloc[:,-1])
        total_value_df[f'{category}'] = tmp_df.sum(axis=1)

print(total_value_df)
print(total_value_df.index.get_loc(pd.to_datetime(datetime.date(2016,6,13)), method='backfill'))
print('===================')
print(total_value_df.iloc[total_value_df.index.get_loc(pd.to_datetime(datetime.date(2016,6,23)), method='nearest')]['bank'])
# print(total_value_df.iloc[datetime.date(2016,6,23)])

# print(total_value_df)

# Plot account values ##########################################################

## Plotly plots ################################################################

### Accounts ###################################################################

fig = go.Figure()

for acct in all_accounts.keys():
    fig.add_trace(go.Scatter(x=all_accounts[acct].date_range,
                        y=all_accounts[acct].calculate_account_values().iloc[:,-1],
                        mode = 'lines',
                        name=accounts_config.get(acct).get('label')))

fig.update_layout(title='Account Balances',
                   xaxis_title='Month',
                   yaxis_title='USD',
                   plot_bgcolor='#f2e9e1',
                   hovermode='x')

fig.update_yaxes(tickprefix="$",
                autorange=True)

fig.show()
# fig.write_image("output/account_totals.png")



### Categories #################################################################
fig = go.Figure()

for category in categories:

    fig.add_trace(go.Scatter(x=total_value_df.index,
                        y=total_value_df[category],
                        mode = 'lines',
                        name=category))



for annotation in category_annotations:
    if 'point_to' in annotation:
        max_value_plotted = total_value_df.to_numpy().max()
        account = annotation['point_to']

        fig.add_annotation(
            xref='x',
            x = annotation['date'],
            yref = 'y',
            y = total_value_df.iloc[total_value_df.index.get_loc(annotation['date'], method='backfill')][account],

            axref='x',
            ax = annotation['date'],
            ayref='y',
            ay = 1.1*max_value_plotted,

            text=annotation['text'],
            showarrow=True,
            textangle=-45,
            arrowhead=2,
        )
    else:
        fig.add_annotation(
            xref='x',
            x = annotation['date'],
            yref = 'y domain',
            y = 0.95,

            # axref='x',
            # ax = annotation['date'],
            # ayref='y',
            # ay = 1.1*max_value_plotted,

            text=annotation['text'],
            showarrow=False,
            textangle=-45,
            arrowhead=2,
        )
fig.update_layout(title='Savings Categories',
                   xaxis_title='Month',
                   yaxis_title='USD',
                   plot_bgcolor='#f2e9e1',
                   hovermode='x')

fig.update_yaxes(tickprefix="$",
                autorange=True)

fig.show()
fig.write_image("output/category_totals.png")

## Matplotlib Plots ############################################################
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
# # plt.plot(thrivent.date_range,
# #          thrivent.calculate_account_values().total_value, '-')
# # plt.plot(brokerage.date_range,
# #          brokerage.calculate_account_values().total_value, '-')
# # plt.plot(metron_401k.date_range,
# #          metron_401k.calculate_account_values().total_value, '-')
# # plt.xlabel("Feature")


# plt.ylabel("US Dollars")
# plt.savefig('output/values.png')
# plt.show()

# Output CSVs ##################################################################
# for account in accounts:
#     all_accounts[account].calculate_account_values().to_csv(f'./output/{account}_529_values.csv')
