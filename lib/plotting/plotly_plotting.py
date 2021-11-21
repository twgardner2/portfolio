from lib.config.config import *
import plotly.graph_objects as go


# Plotly plots ################################################################
def make_plotly_plots(all_accounts, total_value_df):
    ## Accounts ###################################################################

    fig = go.Figure()

    for acct in all_accounts.keys():
        fig.add_trace(go.Scatter(x=all_accounts[acct].date_range,
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
    # fig.write_image("output/account_totals.png")



    ### Categories #################################################################
    fig = go.Figure()

    # for category in categories:
    for category in total_value_df.columns:

        fig.add_trace(go.Scatter(x=total_value_df.index,
                            y=total_value_df[category],
                            mode = 'lines',
                            name=category))



    for annotation in category_annotations:
        if 'point_to' in annotation:
            max_value_plotted = total_value_df.to_numpy().max()
            account = annotation['point_to']

            fig.add_annotation(
                xref='x',
                x = annotation['date'],
                yref = 'y',
                y = total_value_df.iloc[total_value_df.index.get_loc(annotation['date'], method='backfill')][account],

                axref='x',
                ax = annotation['date'],
                ayref='y',
                ay = 1.1*max_value_plotted,

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
