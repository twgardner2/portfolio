from lib.config.config import *
import plotly.graph_objects as go


# Plotly plots ################################################################
def make_plotly_accounts_plot(all_accounts):
    ## Accounts ###################################################################

    fig = go.Figure()

    for acct in all_accounts.keys():
        fig.add_trace(go.Scatter(x=all_accounts[acct].calculate_account_values().index,
                            y=all_accounts[acct].calculate_account_values().iloc[:,-1],
                            mode = 'lines',
                            name=accounts_config.get(acct).get('label')))

    fig.update_layout(title='Account Balances',
                    xaxis_title='Month',
                    yaxis_title='USD',
                    plot_bgcolor='#f2e9e1',
                    hovermode='x')

    fig.update_yaxes(tickprefix="$",
                    autorange=True)

    fig.show()
    fig.write_image("output/account_totals.png")



### Categories #################################################################
def make_plotly_categories_plot(total_value_df):
    fig = go.Figure()

    # for category in categories:
    for category in total_value_df.columns:

        fig.add_trace(go.Scatter(x=total_value_df.index,
                            y=total_value_df[category],
                            mode = 'lines',
                            name=category))

    # Add trace for total
    fig.add_trace(go.Scatter(x=total_value_df.index,
                        y=total_value_df.sum(axis=1),
                        mode = 'lines',
                        name='Total',
                        line=dict(color='blue')))

    # Add trace for total excluding home equity
    fig.add_trace(go.Scatter(x=total_value_df.index,
                        y=total_value_df.sum(axis=1) - total_value_df['home_equity'],
                        mode = 'lines',
                        name='Total (excluding Home Equity)',
                        line=dict(color='blue', dash='dot')))


    for annotation in category_annotations:
        if 'point_to' in annotation:
            max_value_plotted = total_value_df.to_numpy().max()
            account = annotation['point_to']

            fig.add_annotation(
                xref='x',
                x = annotation['date'],
                yref = 'y',
                y = total_value_df.loc[total_value_df.index.asof(annotation['date']), account],

                axref='x',
                ax = annotation['date'],
                ayref='y',
                ay = 1.5*max_value_plotted,

                text=annotation['text'],
                showarrow=True,
                textangle=-45,
                arrowhead=2,
            )
        else:
            fig.add_annotation(
                xref='x',
                    x = annotation['date'],
                    yref = 'y domain',
                    y = 0.95,

                    # axref='x',
                    # ax = annotation['date'],
                    # ayref='y',
                    # ay = 1.1*max_value_plotted,

                text=annotation['text'],
                showarrow=False,
                textangle=-45,
                    arrowhead=2,
            )
    fig.update_layout(title='Savings Categories',
                    xaxis_title='Month',
                    yaxis_title='USD',
                    plot_bgcolor='#f2e9e1',
                    hovermode='x')

    fig.update_yaxes(tickprefix="$",
                    autorange=True)

    fig.show()
    fig.write_image("output/category_totals.png")

def make_plotly_single_account_plot(inv_acct):

    fig = go.Figure()

    # print(inv_acct)
    # print(inv_acct.calculate_account_values())

    for inv in inv_acct.calculate_account_values().columns:
        # print(inv)
        fig.add_trace(go.Scatter(x=inv_acct.calculate_account_values().index,
                    y=inv_acct.calculate_account_values()[inv],
                    mode = 'lines',
                    name=inv))
    fig.show()

