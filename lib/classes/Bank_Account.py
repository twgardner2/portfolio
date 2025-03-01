import pandas as pd
import lib.util.util as util
import datetime


class Bank_Account:
    '''Class to represent a bank account'''

    def __init__(self, name, balances, category):
        self.name = name
        self.category = category
        self.balances = balances[name]
        self.start_date = util.previous_first_of_month(
            self.balances.index.min())
        self.end_date = datetime.date.today()
        self.date_range = util.date_range_generator(
            self.start_date, self.end_date)

    def __str__(self):
        last_month_values = self.calculate_account_values().iloc[-1]

        banner = f"========== Account: {self.name} =========="
        footer = "=" * len(banner)

        result = \
            "\n" + banner + "\n" +\
            f"* Account: {self.name}\n" \
            f"* Category: {self.category}\n" \
            f"* Values as of {last_month_values.name.date()}:\n" \
            f"{last_month_values.to_string()}\n" +\
            footer

        return (result)

    def calculate_account_values(self):

        # Filter balances data on date range
        # (home_equity data goes out to end of mortgage)
        mask = self.balances.index.isin(self.date_range)
        df = self.balances.loc[mask]

        # Rename balance to f'{self.name}_total_value'
        try:
            df = df.to_frame()
        except Exception:
            pass
        df = df.rename({f'{self.name}': f'{self.name}_total_value'}, axis=1)

        return (df)
