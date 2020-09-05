import datetime
from dateutil.relativedelta import relativedelta
import csv
import pandas as pd
import requests
import json
from lib.api.construct_price_history import construct_price_history
import lib.calc.calc as calc
import lib.util.util as util
# import matplotlib.pyplot as plt
from pprint import pprint

# Environment Variables ###########################
# Determine date bounds
start_date = datetime.date(2010, 5, 1)

today = datetime.date.today()
# end_date = datetime.date(today.year, today.month + 1, 1)
end_date = datetime.date(today.year, 4, 1)
###################################################

# Read data #######################################
transactions = util.read_timeseries_csv('./data/transactions.csv')

prices = util.read_timeseries_csv('./data/prices.csv')

positions = transactions["symbol"].unique()
accounts = transactions["account"].unique()

###################################################
date_range = util.date_range_generator(start_date, end_date)


class Account:
    def __init__(self, name, date_range, transactions, prices):
        self.name = name
        self.date_range = date_range
        self.transactions = transactions
        self.prices = prices

    def dummy_method(self):
        print(f'This is a dummy method to print out the name: {self.name}')

    def values_method(self):
        pass

    @staticmethod
    def calculate_shares(date, account, symbol, transactions):
        '''Calculates the number of shares of a symbol on a date'''
        symbol_transactions = transactions.query(
            'symbol == @symbol & account == @account & date <= @date')  #
        shares = symbol_transactions['shares'].sum()

        return (shares)

    def construct_shares_df(self):
        '''Constructs df of shares for each symbol over date_range for account'''

        df = pd.DataFrame(index=self.date_range)

        account_transactions = transactions.query('account == @self.name')
        # print(account_transactions)
        account_symbols = account_transactions['symbol'].unique()
        # print(account_symbols)

        for symbol in account_symbols:
            symbol_shares = []
            for date in self.date_range:
                shares_amount = self.calculate_shares(
                    date, self.name, symbol, self.transactions)
                symbol_shares.append(shares_amount)

            df[symbol] = symbol_shares

        # df.set_index('date')
        # print(df)
        return(df)

    def calculate_account_values(self):
        ''' Calculates the value of shares and the entire account given a date
        indexed dataframe of shares and the date indexed dataframe of position
        prices '''
        account_shares = self.construct_shares_df()
        account_symbols = account_shares.columns

        account_prices = self.prices.loc[:, account_symbols]

        df = account_shares.merge(account_prices,
                                  left_index=True,
                                  right_index=True,
                                  how='left',
                                  suffixes=('_shares', '_price'))

        for symbol in account_symbols:
            df[f'{symbol}_value'] = df[f'{symbol}_shares'] * \
                df[f'{symbol}_price']

        df['total_value'] = df.filter(regex='_value$').sum(axis=1)

        return(df)


t_ira = Account('t_ira', date_range, transactions, prices)
j_ira = Account('j_ira', date_range, transactions, prices)
brokerage = Account('brokerage', date_range, transactions, prices)
# print(j_ira.construct_shares_df())
# print(t_ira.construct_shares_df())

# print(t_ira.calculate_account_values())
print(brokerage.calculate_account_values())

# Create dict of dfs of account values ####

# all_accounts = {}

# for index, account in enumerate(accounts):
#     shares = calc.construct_shares_df(date_range, account, transactions)
#     values = calc.calculate_account_values(shares, prices)
#     all_accounts[account] = values

# pprint(all_accounts)
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
