import pandas as pd
import lib.util.util as util
import sys
import re
import datetime


class Home_Equity:
    def __init__(self, name, home_equity, category):
        self.name = name
        self.category = category

        self.home_equity = home_equity.filter(regex=name)
        self.home_equity = self.home_equity.rename(
            columns=lambda x: re.sub(f'_{name}', '', x))

        self.sold = (self.home_equity['note'] == 'sold').any()

        self.end_date = pd.to_datetime('today').date()

        self.start_date = util.previous_first_of_month(
            self.home_equity.index.min())

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

        # Filter home_equity data on date range
        # (home_equity data goes out to end of mortgage)
        mask = self.home_equity.index.isin(self.date_range)
        df = self.home_equity.loc[mask]

        # The following assignments give false SettingWithCopyWarnings, disable,
        # then reenable below
        original_SettingWithCopyWarning_value = pd.options.mode.chained_assignment
        pd.options.mode.chained_assignment = None

        # Fill latest market_value does for life of mortgage
        df.loc[:, 'market_value'] = df.loc[:, 'market_value'].ffill(axis=0)

        # Calculate total_value (equity = market value - principal)
        df.loc[:, f'{self.name}_total_value'] = df.apply(
            lambda row: row.loc['market_value'] - row.loc['mortgage_principal'], axis=1)

        # Reenable SettingWithCopyWarnings
        pd.options.mode.chained_assignment = original_SettingWithCopyWarning_value

        return (df)
