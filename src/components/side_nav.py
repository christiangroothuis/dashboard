import dash
from dash import Output, Input, State, html
import dash_mantine_components as dmc
from jupyter_dash import JupyterDash
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_core_components as dcc

button = dbc.Button(
    children=[DashIconify(icon="ci:hamburger-lg", width=24, height=24, color="#c2c7d0")],
    id='sidebar-button',
    style={'background-color': 'white', 'border': 'none', 'margin-left': '15px'},
)

side_bar = html.Div(
        html.Div(
            html.H4('Clustering', style={'padding': '10px', 'border-bottom': '1px solid white'}),
        className='slide-in-content', id='slide-in-content'),
    className='slide-in', id='slide-in',
)

@dash.callback(
    Output('slide-in', 'className'),
    [Input('sidebar-button', 'n_clicks')],
    [State('slide-in', 'className')],
    prevent_initial_call=True,
    suppress_callback_exceptions=True
)
def toggle_slide_in(opened, current_class):
    print(opened)
    if opened % 2 == 1:
        return f"{current_class} show"  # Show the sidebar by adding the 'show' class
    else:
        print('close')
        return current_class.replace('show', '')  # Hide the sidebar by removing the 'show' class





"""
@dash.callback(
    Output("slide-in", "style"),  # what we wanted to change
    Input("sidebar-button", "n_clicks"),  # width will change when btn is triggered
    State('slide-in', 'style'),  # store inital width
    prevent_initial_call=True,
)
def sidebar(opened, style):
    if opened:
        if style['display'] == 'none':  # if initial width is 300 then return 70
            style['display'] = 'block'
        else:
            style['display'] = 'none'
    return style

"""