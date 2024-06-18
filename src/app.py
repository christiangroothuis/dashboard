import dash
from dash import html
from layout import dash_layout
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(dash_layout, id='app_container')

server = app.server  # Expose the server for gunicorn

if __name__ == "__main__":
    app.run(
        debug=True,
        port="2030",
        dev_tools_hot_reload=True,
        dev_tools_hot_reload_interval=100,
    )
