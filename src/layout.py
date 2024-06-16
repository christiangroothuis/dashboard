# External imports
import dash_bootstrap_components as dbc
from dash import html, State

# Internal imports
from components.map_tabs import map_tabs_layout
from components.side_nav import button, side_bar  # getAppHeader # side_navbar, Btn1
from components.line_graph import line_graph_layout
from components.h_bar_chart import h_barchart_layout
from components.map_tabs import choropleth_map_layout
from components.correlation_graph import correlation_graph_layout

# from components.scripts.data_preprocessing import geo_data, df_pas_original, df_pas_granular, df_outcomes, df_stop_search, \
#    df_street, df_economic, df_ethnicity


# ====================================
# Create the layout
# ====================================

from dash import dcc

# dash_layout = dbc.Container([
#     html.Link(href='/assets/styles.css', rel='stylesheet'),
#     dcc.Store(id='stored_data', data=[]),  # Store to hold selected boroughs
#     dcc.Store(id='selected_borough', data=[]),
#
#     dbc.Row([
#         dbc.Row(html.H1('Powered by the TU/e', className='top-panel')),
#         dbc.Row(html.H1('𝓟oL𝛔cal', className='polocal-header', style={'margin-top': '24px'})),
#         dbc.Row(dbc.Navbar([button, *map_tabs_layout], style={'margin-top': '-20px', 'padding': 0}),
#                 className="dbc-navbar", )
#     ], className="mb-2"),
#     dbc.Row([
#         dbc.Col(side_bar, id='sidebar-column', width=0),
#         dbc.Col([
#             dbc.Row([dcc.RangeSlider(2015, 2021, 1,
#                                 value=[2017, 2018],
#                                 id='range-slider',
#                                 marks= {i: str(i) for i in range(2015, 2022, 1)},
#                                 ),], style={'padding': '5px'}),
#             dbc.Row([
#                 dbc.Col(choropleth_map_layout, id='map-column'),
#                 dbc.Col(h_barchart_layout, id='h-barchart-column', className='graph-container'),
#             ]),
#
#         ]),
#     ]),
#     dbc.Row([
#         dbc.Col(line_graph_layout),
#         dbc.Col(correlation_graph_layout),
#     ]),
#
# ], fluid=True, className='container')
# dash_layout = dbc.Container([
#     html.Link(href='/assets/styles.css', rel='stylesheet'),
#     dcc.Store(id='stored_data', data=[]),  # Store to hold selected boroughs
#     dcc.Store(id='selected_borough', data=[]),
#     dcc.Store(id='shared-data-store', data=[]),  # New store for shared data
#
#     dbc.Row([
#         dbc.Row(html.H1('Powered by the TU/e', className='top-panel')),
#         dbc.Row(html.H1('𝓟oL𝛔cal', className='polocal-header', style={'margin-top': '24px'})),
#         dbc.Row(dbc.Navbar([button, *map_tabs_layout], style={'margin-top': '-20px', 'padding': 0}),
#                 className="dbc-navbar", )
#     ], className="mb-2"),
#     dbc.Row([
#         dbc.Col(side_bar, id='sidebar-column', width=0),
#         dbc.Col([
#             dbc.Row([dcc.RangeSlider(2015, 2021, 1,
#                                 value=[2017, 2018],
#                                 id='range-slider',
#                                 marks={i: str(i) for i in range(2015, 2022, 1)},
#                                 ),], style={'padding': '5px'}),
#             dbc.Row([
#                 dbc.Col(choropleth_map_layout, id='map-column'),
#                 dbc.Col(h_barchart_layout, id='h-barchart-column', className='graph-container'),
#             ]),
#
#         ]),
#     ]),
#     dbc.Row([
#         dbc.Col(line_graph_layout),
#         dbc.Col(correlation_graph_layout),
#     ]),
#
# ], fluid=True, className='container')


dash_layout = dbc.Container([
    html.Link(href='/assets/styles.css', rel='stylesheet'),
    dcc.Store(id='stored_data', data=[]),  # Store to hold selected boroughs
    dcc.Store(id='selected_borough', data=[]),
    dcc.Store(id='shared-data-store', data=[]),  # Store for shared data


    dbc.Row([
        dbc.Row(html.H1('Powered by the TU/e', className='top-panel')),
        dbc.Row(html.H1('𝓟oL𝛔cal', className='polocal-header', style={'margin-top': '24px'})),
        dbc.Row(dbc.Navbar([button, *map_tabs_layout], style={'margin-top': '-20px', 'padding': 0}),
                className="dbc-navbar", )
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(side_bar, id='sidebar-column', width=0),
        dbc.Col([
            dbc.Row([dcc.RangeSlider(2015, 2021, 1,
                                value=[2017, 2018],
                                id='range-slider',
                                marks={i: str(i) for i in range(2015, 2022, 1)},
                                ),], style={'padding': '5px'}),
            dbc.Row([
                dbc.Col(choropleth_map_layout, id='map-column'),
                dbc.Col(h_barchart_layout, id='h-barchart-column', className='graph-container'),
            ]),

        ]),
    ]),
    dbc.Row([
        dbc.Col(line_graph_layout),
        dbc.Col(correlation_graph_layout),
    ]),

], fluid=True, className='container')

