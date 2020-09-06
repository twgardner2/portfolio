import pandas as pd


class Account:
    def __init__(self, name, date_range, transactions, prices):
        self.name = name
        self.date_range = date_range
        self.transactions = transactions
        self.prices = prices

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

        account_transactions = self.transactions.query('account == @self.name')
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
