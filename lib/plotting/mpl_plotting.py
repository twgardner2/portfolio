import matplotlib.pyplot as plt


def make_matplotlib_plots(all_accounts):
    ## Matplotlib Plots ############################################################
    for account in all_accounts.keys():
        plt.plot(all_accounts[account].date_range,
                 all_accounts[account].calculate_account_values()[f'{account}_total_value'], '-')

    plt.ylabel("US Dollars")
    plt.savefig('output/values.png')
    plt.show()
