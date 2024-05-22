from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
from components.map2 import map_layout
from components.horizontal_barchart import h_barchart_layout
from components.line_chart import linechart_layout
from components.bar_chart import barchart_layout

import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

# Sample data for the charts (replace with your actual data)
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 1, 3, 4, 2],
    'category': ['A', 'B', 'A', 'B', 'A']
})

# Sample data for the map
borough_data = {
    'Borough': ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden', 'Croydon', 'Ealing', 'Enfield', 'Greenwich'],
    'Latitude': [51.5541, 51.6538, 51.4416, 51.5634, 51.4028, 51.5290, 51.3714, 51.5130, 51.6526, 51.4892],
    'Longitude': [0.1505, -0.2003, 0.1505, -0.2758, 0.0148, -0.1255, -0.0989, -0.3080, -0.0810, 0.0648]
}

# Create DataFrame
df_boroughs = pd.DataFrame(borough_data)

# Define the layout for the map
map_layout = go.Layout(
    mapbox_style="open-street-map",
    mapbox_zoom=10,
    mapbox_center={"lat": 51.5074, "lon": -0.1278}
)

# Create the scatter map figure
map_fig = go.Figure(go.Scattermapbox(
    lat=df_boroughs['Latitude'],
    lon=df_boroughs['Longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=df_boroughs['Borough'],
))

# Update the layout of the map figure
map_fig.update_layout(map_layout)

# Sample data for demonstration purposes
df_granular_pas = pd.read_csv('../data/pas_data_ward_level/PAS_ward_level_FY_20_21.csv')
# df_grouped = df_granular_pas.groupby(['Borough', 'Q1']).size().unstack().fillna(0)

# Grouping the data
df_grouped = df_granular_pas.groupby(['Borough', 'Q1']).size().unstack().fillna(0)

# Create the interactive bar chart
h_barchart_fig = px.bar(
    df_grouped,
    y=df_grouped.index,
    x=df_grouped.columns,
    labels={'value': 'Count', 'Borough': 'Borough'},
    title='Distribution of trust in neighbourhood per borough'
)
h_barchart_fig.update_layout(barmode='stack')

# Create figures using Plotly Express
barchart_fig = px.scatter(df, x='x', y='y', color='category')

linechart_fig = px.line(df, x='x', y='y')

# Define the layout
dash_layout = [
    # Heading
    html.Div([
        html.H1('Welcome to Poloc!', style={'color': '#243E4C', 'display': 'block', 'textAlign': 'center'}),
    ]),

    html.Div([
        html.Div(dcc.Graph(id='map', figure=map_fig, style={'height': '500px'}), style={'flex': '1'}),
        html.Div(dcc.Graph(id='barchart', figure=barchart_fig, style={'height': '500px'}), style={'flex': '1'}),
    ], style={'display': 'flex', 'width': '100%'}),

    html.Div([
        html.Div(dcc.Graph(id='h_barchart', figure=h_barchart_fig, style={'height': '500px'}), style={'flex': '1'}),
        html.Div(dcc.Graph(id='linechart', figure=linechart_fig, style={'height': '500px'}), style={'flex': '1'}),
    ], style={'display': 'flex', 'width': '100%'}),
]