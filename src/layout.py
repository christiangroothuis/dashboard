from dash import dcc, callback, Output, Input, callback_context, State
import dash_bootstrap_components as dbc
import plotly.express as px

# Internal imports
from components.map_tabs import map_tabs_layout
from components.side_nav import button, side_bar # getAppHeader # side_navbar, Btn1
from components.scripts.import_data import df_data, geo_data
from components.scripts.map_categories import map_categories_dict
from dash import html


# ====================================
# Create the layout
# ====================================

dash_layout = dbc.Container([
    html.Link(href='/assets/styles.css', rel='stylesheet'),
    dbc.Row([
        dbc.Row(html.H1('Powered by the TU/e', className='top-panel')),
        dbc.Row(html.H1('𝓟oL𝛔cal', className='polocal-header', style={'margin-top': '24px'})),
        dbc.Row(dbc.Navbar([button, *map_tabs_layout], style={'margin-top': '-20px', 'padding': 0}
        ), className="dbc-navbar",)
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(side_bar, style={'width': '100px'}),
        dbc.Col(dcc.Graph(id="choropleth-map"),  style={'width': '900px'}, width=4),
    ])
], fluid=True, className='container')


def find_button_attribute(attributes: tuple, button_id: str):
    sub_attribute = '"Good Job" local'
    for i, attribute in attributes:
        if i == button_id:
            sub_attribute = attribute
    return sub_attribute


# Define callback to update map based on dropdown selection
@callback(
    Output("choropleth-map", "figure"),
    [Input(str(i), "n_clicks") for i in range(10)]
)
def update_map(*args):
    """
    Updates the choropleth plot based on the nested dropdown.
    :param args: the IDs of all selectable categories in the nested drop-downs.
    :return: choropleth plot.
    """
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # Find out what attribute should be displayed in plot depending on IDs of type str(int).
    if button_id is None:
        sub_attribute = '"Good Job" local'  # Default to Trust_score if no button is clicked
    elif 0 <= int(button_id) <= 4:
        attributes = map_categories_dict['PAS']['Confidence']
        sub_attribute = find_button_attribute(attributes, button_id)
    elif 5 <= int(button_id) <= 7:
        attributes = map_categories_dict['PAS']['Trust']
        sub_attribute = find_button_attribute(attributes, button_id)
    elif 8 <= int(button_id) <= 9:
        attributes = map_categories_dict['PAS']['Other']
        sub_attribute = find_button_attribute(attributes, button_id)
    else:
        sub_attribute = None

    if sub_attribute is None:
        sub_attribute = '"Good Job" local'  # Default to Trust_score if no button is clicked

    # Define the choropleth plot
    fig = px.choropleth(
        data_frame=df_data, geojson=geo_data, locations="Borough", featureidkey="properties.name",
        color=sub_attribute, color_continuous_scale='viridis',
        projection="mercator")
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                      width=800,
                      height=600)

    fig.update_coloraxes(colorbar_len=0.5)

    return fig



