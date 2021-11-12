from dateutil.relativedelta import relativedelta
import pandas as pd
import lib.util.util as util



class Account:
    def __init__(self, name, trans, prices, date_range, category):
        self.name = name
        self.category = category
        self.trans = trans[trans['account']==name]
        self.symbols = self.trans['symbol'].unique()
        self.start_date = util.previous_first_of_month(self.trans.index.min())
        self.start_date = pd.to_datetime(self.start_date)
        self.end_date = pd.to_datetime('today')
        self.date_range = util.date_range_generator(self.start_date, self.end_date)
        self.prices = prices.loc[prices.index>=self.start_date, self.symbols]

    @staticmethod
    def calculate_shares_on_date(date, symbol, trans):
        '''Calculates the number of shares of a symbol on a date'''

        # Filter transactions for symbol and those before 'date', sort by 'date'
        symbol_trans = trans.loc[
                            (trans.index<=date) & 
                            (trans.symbol==symbol), 
                        ].sort_values(by='date')

        # Initialize shares to 0
        shares = 0

        # Iterate over filtered transactions
        for index, row in symbol_trans.iterrows():
            # Stock increases
            if row['type'].strip() in ['purchase', 'div_reinvest', 'stock_dividend', 'ltcp_reinvest']:
                shares = shares + abs(float(row['shares']))
            # Stock decreases
            elif row['type'].strip() in ['sale', 'fee']:
                if row['shares'].strip() == 'all':
                    shares = 0
                else:
                    shares = shares - abs(float(row['shares']))
            # Splits
            elif row['type'] in ['split']:
                shares = shares * float(row['shares'])

        return (shares)
    

    def construct_shares_df(self):
        '''Constructs df of shares for each symbol over date_range for 
        account'''

        # Create dataframe to populate
        df = pd.DataFrame(index=self.date_range, columns=self.symbols)

        # Iterate over symbols in account
        for symbol in self.symbols:
            # Calculate shares on starting date
            df[symbol].iloc[0] = self.calculate_shares_on_date(df.iloc[0].name, symbol, self.trans)

            symbol_trans = self.trans[self.trans['symbol']==symbol]

            # Iterate over index of dataframe to populate
            for i, date in enumerate(df.index):
                # Skip first row which we already populated
                if i==0:
                    continue
                
                period_trans = symbol_trans[
                                    (symbol_trans.index>df.index[i-1]) &
                                    (symbol_trans.index<=df.index[i])
                                ].sort_values(by='date')

                # Shares at beginning of period
                shares  = df[symbol].iloc[i-1]

                for index, row in period_trans.iterrows():
                    if row['type'] in ['purchase', 'div_reinvest', 'stock_dividend', 'ltcp_reinvest']:
                        shares += abs(float(row['shares']))
                    elif row['type'] in ['sale', 'fee']:
                        if row['shares'] == 'all':
                            shares = 0
                        else:
                            shares += -abs(float(row['shares']))
                    elif row['type'] in ['split']:
                        shares += shares*(abs(float(row['shares']))-1)
                df[symbol].iloc[i] = shares

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

        df[f'{self.name}_total_value'] = df.filter(regex='_value$').sum(axis=1)
        df = df.filter(regex='_value$')

        return(df)
