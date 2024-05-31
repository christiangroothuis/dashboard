import dash
from dash import html
from layout import dash_layout
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_layout = html.Div([
    html.Div([choropleth_map_layout], style={"width": "50%", "display": "inline-block"}),
    html.Div([line_graph_layout], style={"width": "50%", "display": "inline-block"})
])

app.layout = html.Div(dash_layout, id='app_container')

app.run(debug=True, port=2030, dev_tools_hot_reload=False, dev_tools_hot_reload_interval=100)
