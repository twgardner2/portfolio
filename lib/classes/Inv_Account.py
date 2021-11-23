import pandas as pd
import numpy as np
import lib.util.util as util



class Inv_Account:
    def __init__(self, name, trans, prices, category):
        self.name = name
        self.category = category
        self.trans = trans[trans['account']==name]
        self.symbols = self.trans['symbol'].unique()
        self.start_date = util.previous_first_of_month(self.trans.index.min())
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
        for i in range(len(symbol_trans)):
            # Stock increases
            if symbol_trans.iloc[i]['type'].strip() in ['purchase', 'div_reinvest', 'stock_dividend', 'ltcp_reinvest']:
                shares = shares + abs(float(symbol_trans.iloc[i]['shares']))
            # Stock decreases
            elif symbol_trans.iloc[i]['type'].strip() in ['sale', 'fee']:
                if symbol_trans.iloc[i]['shares'].strip() == 'all':
                    shares = 0
                else:
                    shares = shares - abs(float(symbol_trans.iloc[i]['shares']))
            # Splits
            elif symbol_trans.iloc[i]['type'] in ['split']:
                shares = shares * float(symbol_trans.iloc[i]['shares'])

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

            # Get just the trans for the symbol we're working on 
            symbol_trans = self.trans[self.trans['symbol']==symbol]

            # Iterate over index of dataframe to populate
            for i, date in enumerate(df.index):
                # Skip first row which we already populated
                if i==0:
                    continue
                
                # Get the trans for the month
                period_trans = symbol_trans[
                                    (symbol_trans.index>df.index[i-1]) &
                                    (symbol_trans.index<=df.index[i])
                                ].sort_values(by='date')

                # Shares at beginning of period
                shares  = df[symbol].iloc[i-1]

                # Iterate over the month's trans and calculate new shares
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

    def construct_shares_df2(self):
        # Create dataframe to populate
        df = pd.DataFrame(0, index=self.date_range, columns=self.symbols)

        for symbol in self.symbols:
    
            symbol_trans = self.trans[self.trans['symbol']==symbol]
            mask = symbol_trans.index <= self.date_range[-1]
            symbol_trans = symbol_trans.loc[mask]
            while not symbol_trans.empty:

                first_trans_index = symbol_trans.index[0]

                shares_i = df.index.get_loc(first_trans_index, method='backfill')
                shares_value = df.iloc[shares_i-1][symbol]

                shares_date_pre_trans = df.index[shares_i-1]
                shares_date_post_trans = df.index[shares_i]

                # Trans between dates
                trans_between_dates = symbol_trans.loc[shares_date_pre_trans:shares_date_post_trans]

                # Remove trans_between_dates from symbol_trans
                mask = np.invert(symbol_trans.index.isin(trans_between_dates.index))
                symbol_trans = symbol_trans[mask]

                # for i in trans_between_dates.index:
                for i in range(len(trans_between_dates)):
                    # Stock increases
                    if trans_between_dates.iloc[i]['type'].strip() in ['purchase', 'div_reinvest', 'stock_dividend', 'ltcp_reinvest']:
                        shares_value = shares_value + float(trans_between_dates.iloc[i]['shares'])
                    # Stock decreases
                    elif trans_between_dates.iloc[i]['type'].strip() in ['sale', 'fee']:
                        if trans_between_dates.iloc[i]['shares'].strip() == 'all':
                            shares_value = 0
                        else:
                            shares_value = shares_value - abs(float(trans_between_dates.iloc[i]['shares']))
                    # Splits
                    elif trans_between_dates.iloc[i]['type'].strip() in ['split']:
                        shares_value = shares_value * float(trans_between_dates.iloc[i]['shares'])

                mask = [i >= shares_i for i in range(df.index.shape[0])] 
                df.loc[mask,symbol] = shares_value

        return(df)


    def calculate_account_values(self):
        ''' Calculates the value of shares and the entire account given a date
        indexed dataframe of shares and the date indexed dataframe of position
        prices '''
        account_shares = self.construct_shares_df2()
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
