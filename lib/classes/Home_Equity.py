import pandas as pd
import lib.util.util as util


class Home_Equity:
    def __init__(self, name, home_equity, date_range, category):
        self.name = name
        self.category = category

        self.home_equity = home_equity[home_equity['home']==name]
        self.start_date = util.previous_first_of_month(self.home_equity.index.min())
        # self.start_date = pd.to_datetime(self.start_date)
        self.end_date = pd.to_datetime('today')
        self.date_range = util.date_range_generator(self.start_date, self.end_date)

    def calculate_account_values(self):

        # Create dataframe to populate
        # df = pd.DataFrame(index=self.date_range, columns=[self.name])
        df = pd.DataFrame(index=self.date_range)

        df = df.merge(self.home_equity,
                      left_index=True,
                      right_index=True,
                      how='left')
        df = df.drop('home', axis=1)

        df[f'{self.name}_total_value'] = df['market_value'] - df['mortgage_principal']


        return(df)
