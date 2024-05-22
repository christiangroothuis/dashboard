# General Imports
import dash
from dash import html
from layout import dash_layout
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(dash_layout, id='app_container')

app.run(debug=False, port=2030, dev_tools_hot_reload=False, dev_tools_hot_reload_interval=100)
