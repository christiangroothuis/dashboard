# Imports
from dash import dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import os
from pathlib import Path


h_barchart_layout = dcc.Graph(id="h_barchart")

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'pas_data_ward_level/PAS_ward_level_FY_20_21.csv'))
df_grouped = df_granular_pas.groupby(['Borough', 'Q1']).size().unstack().fillna(0)
@callback(
    Output("h_barchart", "figure"),
    [Input(str(i), "n_clicks") for i in range(10)]
)
def update_h_barchart(*args):
    fig = px.bar(
        df_grouped,
        y=df_grouped.index,
        x=df_grouped.columns,
        labels={'value': 'Count', 'Borough': 'Borough'},
        title='Distribution of trust in neighbourhood per borough'
    )
    fig.update_layout(barmode='stack')

    return fig