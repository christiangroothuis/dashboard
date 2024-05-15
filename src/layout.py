from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
from components.map2 import map_layout2
from components.map import map_layout
from components.horizontal_barchart import h_barchart_layout
from components.line_chart import linechart_layout
from components.bar_chart import barchart_layout

import dash_bootstrap_components as dbc


dash_layout = [
    # Heading
    html.Div([html.H1('Welcome to Polocal!', style={'color': '#243E4C', 'display': 'block', 'textAlign': 'center'}),
              ]),

    map_layout2,

    html.Div([
        map_layout,

        html.Div([
            h_barchart_layout
        ], style={'width': '48%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.Div([
            linechart_layout
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            barchart_layout
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),
]

