from dash import Dash, html, dcc, callback, Output, Input, dash_table, callback_context
import pandas as pd
import dash_bootstrap_components as dbc
from urllib.request import urlopen
import json
import plotly.express as px
from components.map_london import map_layout
from components.horizontal_barchart import h_barchart_layout
from components.line_chart import linechart_layout
from components.bar_chart import barchart_layout
from components.scripts.import_data import df_data, geo_data
from components.map_tabs import map_tabs_layout

# Create the layout
dash_layout = dbc.Container([
    dbc.Row([
        *map_tabs_layout,
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="choropleth-map"), width=12)
    ])
], fluid=True)


# Define callback to update map based on dropdown selection
@callback(
    Output("choropleth-map", "figure"),
    [Input('"Good Job" local', "n_clicks"),
     Input('Informed local', "n_clicks"),
     Input('Listen to concerns', "n_clicks"),
     Input('Relied on to be there', "n_clicks"),
     Input('Understand issues', "n_clicks")]
)
def update_map(good_job_local, informed_local, listen_concerns, relied_on, understand_issues):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if button_id == '"Good Job" local':
        sub_attribute = '"Good Job" local'
    elif button_id == 'Contact ward officer':
        sub_attribute = 'Contact ward officer'
    elif button_id == 'Informed local':
        sub_attribute = 'Informed local'
    elif button_id == 'Listen to concerns':
        sub_attribute = 'Listen to concerns'
    else:
        sub_attribute = None

    if sub_attribute is None:
        sub_attribute = '"Good Job" local'  # Default to Trust_score if no button is clicked

    fig = px.choropleth(
        data_frame=df_data, geojson=geo_data, locations="Borough", featureidkey="properties.name",
        color=sub_attribute, color_continuous_scale='viridis',
        projection="mercator")
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})

    return fig