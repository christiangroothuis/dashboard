# General Imports
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
from layout2 import dash_layout

app = Dash(__name__, use_pages=False, suppress_callback_exceptions=True)

app.layout = html.Div(dash_layout, id='app_container')

app.run(debug=False, port=2030, dev_tools_hot_reload=False, dev_tools_hot_reload_interval=100)