# Imports
from dash import dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import os
from pathlib import Path


h_barchart_layout = dcc.Graph(id="h_barchart")

data_directory = os.path.join(Path(os.getcwd()).parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'pas_data_ward_level/PAS_ward_level_FY_20_21.csv'))
df_grouped = df_granular_pas.groupby(['Borough', 'Q1']).size().unstack().fillna(0)
# @callback(
#     Output("h_barchart", "figure"),
#     [Input(str(i), "n_clicks") for i in range(10)]
# )
# def update_h_barchart(*args):
#     fig = px.bar(
#         df_grouped,
#         y=df_grouped.index,
#         x=df_grouped.columns,
#         labels={'value': 'Count', 'Borough': 'Borough'},
#         title='Distribution of trust in neighbourhood per borough'
#     )
#     fig.update_layout(barmode='stack')
#
#     return fig




#Test 2



# @callback(
#     Output("h_barchart", "figure"),
#     Input('stored_BR_data', 'data')
# )
# def update_h_barchart(stored_BR_data):
#     if not stored_BR_data:
#         df_filtered = df_grouped.sum(axis=1).reset_index()
#     else:
#         df_filtered = df_grouped.loc[stored_BR_data].sum(axis=1).reset_index()
#
#     fig = px.bar(
#         df_filtered,
#         y='Borough',
#         x=0,
#         labels={'0': 'Count', 'Borough': 'Borough'},
#         title='Distribution of trust in neighbourhood per borough'
#     )
#     fig.update_layout(barmode='stack')
#     return fig



#Test 3

@callback(
    Output("h_barchart", "figure"),
    Input('stored_BR_data', 'data'),
    prevent_initial_call=True
)
def update_h_barchart(selected_boroughs):
    if not selected_boroughs:
        df_filtered = df_grouped.sum(axis=1).reset_index()
    else:
        df_filtered = df_grouped.loc[selected_boroughs].sum(axis=1).reset_index()

    fig = px.bar(
        df_filtered,
        y='Borough',
        x=0,
        labels={'0': 'Count', 'Borough': 'Borough'},
        title='Distribution of trust in neighbourhood per borough'
    )
    fig.update_layout(barmode='stack')
    return fig
