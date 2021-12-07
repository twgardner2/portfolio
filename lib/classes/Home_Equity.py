import pandas as pd
import lib.util.util as util


class Home_Equity:
    def __init__(self, name, home_equity, category):
        self.name = name
        self.category = category

        self.home_equity = home_equity[home_equity['home']==name]

        self.sold = (self.home_equity['note'] == 'sold').any()

        # if self.sold:
        #     self.home_equity = self.home_equity[self.home_equity['note'] != 'sold']
        #     self.end_date = self.home_equity[self.home_equity['note'] != 'sold'].index.max()
        # else:
        #     self.end_date = pd.to_datetime('today')
        
        self.end_date = pd.to_datetime('today')

        self.start_date = util.previous_first_of_month(self.home_equity.index.min())
        self.date_range = util.date_range_generator(self.start_date, self.end_date)

    def calculate_account_values(self):

        # Filter home_equity data on date range
        # (home_equity data goes out to end of mortgage)
        mask = self.home_equity.index.isin(self.date_range)
        df = self.home_equity.loc[mask]

        # Drop the 'home' column
        df = df.drop('home', axis=1)

        # Fill latest market_value does for life of mortgage
        df['market_value'] = df['market_value'].ffill(axis=0)

        # Calculate total_value (equity = market value - principal)
        df[f'{self.name}_total_value'] = df['market_value'] - df['mortgage_principal']

        return(df)
