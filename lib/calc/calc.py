import pandas as pd


def calculate_shares(date, account, symbol, transactions):
    '''Calculates the number of shares of a symbol on a date'''
    symbol_transactions = transactions.query(
        'symbol == @symbol & account == @account & date <= @date')  #
    shares = symbol_transactions['shares'].sum()

    return (shares)


def construct_shares_df(date_range, account, transactions):
    '''Constructs df of shares for each symbol over date_range for account'''

    df = pd.DataFrame(index=date_range)

    account_transactions = transactions.query('account == @account')
    # print(account_transactions)
    account_symbols = account_transactions['symbol'].unique()
    # print(account_symbols)

    for symbol in account_symbols:
        symbol_shares = []
        for date in date_range:
            shares_amount = calculate_shares(
                date, account, symbol, transactions)
            symbol_shares.append(shares_amount)

        df[symbol] = symbol_shares

    # df.set_index('date')
    # print(df)
    return(df)


def calculate_account_values(shares_df, prices_df):
    ''' Calculates the value of shares and the entire account given a date 
    indexed dataframe of shares and the date indexed dataframe of position 
    prices '''
    account_symbols = shares_df.columns

    account_prices = prices_df.loc[:, account_symbols]

    df = shares_df.merge(account_prices,
                         left_index=True,
                         right_index=True,
                         how='left',
                         suffixes=('_shares', '_price'))

    for symbol in account_symbols:
        df[f'{symbol}_value'] = df[f'{symbol}_shares'] * df[f'{symbol}_price']

    df['total_value'] = df.filter(regex='_value$').sum(axis=1)

    return(df)


def calculate_grand_total_value(all_accounts):
    grand_total = pd.DataFrame()
