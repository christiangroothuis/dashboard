# General Imports
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
from layout import dash_layout
import dash_bootstrap_components as dbc
# from components.dropdown2 import navbar, dropdown_menu


# app = Dash(__name__, use_pages=False, suppress_callback_exceptions=True)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(dash_layout, id='app_container')
# dash_layout,
app.run(debug=False, port=2030, dev_tools_hot_reload=False, dev_tools_hot_reload_interval=100)
