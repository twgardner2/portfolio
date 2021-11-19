import pandas as pd
import lib.util.util as util


class Bank_Account:
    def __init__(self, name, balances, date_range, category):
        self.name = name
        self.category = category
        self.balances = balances[balances['account'] == name]
        self.start_date = util.previous_first_of_month(self.balances.index.min())
        self.start_date = pd.to_datetime(self.start_date)
        self.end_date = pd.to_datetime('today')
        self.date_range = util.date_range_generator(self.start_date, self.end_date)

    def calculate_account_values(self):

        # Create dataframe to populate
        df = pd.DataFrame(index=self.date_range)

        df = df.merge(self.balances,
                        left_index = True,
                        right_index = True,
                        how = 'left')
        df = df.drop('account', axis=1)
        df = df.rename({'balance': f'{self.name}_total_value'}, axis=1)


        return(df)
