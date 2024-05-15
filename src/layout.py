from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
from components.map import map_layout
import dash_bootstrap_components as dbc


dash_layout = [
    # Heading
    html.Div([html.H1('Welcome to Polocal!', style={'color': '#243E4C', 'display': 'block', 'textAlign': 'center'}),
              ]),

    # Map
    map_layout,

    # Horizontal barchart


    # Line chart


    # Grouped bar chart


]


