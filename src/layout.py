# External imports
import dash_bootstrap_components as dbc

# Internal imports
from components.map_tabs import map_tabs_layout
from components.side_nav import button, side_bar # getAppHeader # side_navbar, Btn1
from components.line_graph import line_graph_layout
from components.correlation_graph import correlation_graph_layout
from components.h_bar_chart import h_barchart_layout
from components.map_tabs import choropleth_map_layout
from dash import html , State


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
        dbc.Col(choropleth_map_layout, id='map-column', width=6),
        dbc.Col(h_barchart_layout, id='h-barchart-column', width=3),
    ]),
    dbc.Row([
        dbc.Col(correlation_graph_layout),
        dbc.Col(line_graph_layout),
    ])
], fluid=True, className='container')
# dash_layout = dbc.Container([
#     html.Link(href='/assets/styles.css', rel='stylesheet'),
#     dbc.Row([
#         dbc.Row(html.H1('Powered by the TU/e', className='top-panel')),
#         dbc.Row(html.H1('𝓟oL𝛔cal', className='polocal-header', style={'margin-top': '24px'})),
#         dbc.Row(dbc.Navbar([button, *map_tabs_layout], style={'margin-top': '-20px', 'padding': 0}
#         ), className="dbc-navbar",)
#     ], className="mb-2"),
#     dbc.Row([
#         # Sidebar column
#         dbc.Col(side_bar, id='sidebar-column', width=2),
#         # Map column
#         dbc.Col(choropleth_map_layout, id='chloropleth_map', width=4),
#         # Horizontal bar chart column
#         dbc.Col(h_barchart_layout, id='h-barchart', width=2),
#     ]),
#     dbc.Row([
#         dbc.Col(correlation_graph_layout),
#         dbc.Col(line_graph_layout),
#     ])
# ], fluid=True, className='container')


        #
        # dbc.Col(side_bar, id='sidebar-column', style={'width': '100px'}),  # Column for the sidebar
        # dbc.Col([choropleth_map_layout, h_barchart_layout], id='map-barchart-column'),
        # # Column for the map and bar chart
#     ]),
#     dbc.Row([
#         dbc.Col(correlation_graph_layout),
#         dbc.Col(line_graph_layout),
#     ])
# ], fluid=True, className='container')
#












