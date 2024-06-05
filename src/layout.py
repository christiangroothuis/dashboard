# External imports
import dash_bootstrap_components as dbc
from dash import html , State

# Internal imports
from components.map_tabs import map_tabs_layout
from components.side_nav import button, side_bar # getAppHeader # side_navbar, Btn1
from components.line_graph import line_graph_layout
from components.h_bar_chart import h_barchart_layout
from components.map_tabs import choropleth_map_layout


# ====================================
# Create the layout
# ====================================

from dash import dcc

dash_layout = dbc.Container([
    html.Link(href='/assets/styles.css', rel='stylesheet'),
    dcc.Store(id='stored_BR_data', data=[]),  # Store to hold selected boroughs
    dbc.Row([
        dbc.Row(html.H1('Powered by the TU/e', className='top-panel')),
        dbc.Row(html.H1('𝓟oL𝛔cal', className='polocal-header', style={'margin-top': '24px'})),
        dbc.Row(dbc.Navbar([button, *map_tabs_layout], style={'margin-top': '-20px', 'padding': 0}), className="dbc-navbar",)
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(side_bar, id='sidebar-column', width=3),
        dbc.Col(
            dbc.Row([
                dbc.Col(choropleth_map_layout, id='map-column'),
                dbc.Col(h_barchart_layout, id='h-barchart-column', className='graph-container'),
            ]),

        ),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='correlation-graph', className='graph-container')),

        dbc.Col(line_graph_layout),
    ]),

], fluid=True, className='container')