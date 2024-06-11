# Imports
from dash import dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import os
from pathlib import Path

# from .scripts.import_data import df_pas_granular as df_granular_pas

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'pas_granular.csv'))

h_barchart_layout = dcc.Graph(id="h_barchart")

df_grouped = df_granular_pas.groupby(['Borough', 'Ss Agree Neither Agree Nor Disagree']).size().unstack().fillna(0)

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

    )
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=600  # Set a specific height for consistency
    )
    fig.update_layout(barmode='stack')
    return fig
