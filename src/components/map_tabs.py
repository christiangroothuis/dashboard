import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, callback_context, dcc
from .scripts.map_categories import map_categories_dict
import plotly.express as px
from .scripts.import_data import df_data, geo_data


def create_nested_dropdown(map_categories_dict: dict, key_path: list):
    """
    Recursively defines the children of the DropdownMenu.
    :param map_categories_dict: dictionary of all attributes to be displayed.
    :param key_path: list of keys contained in map_categories_dict.
    :return: children of its parent DropdownMenu.
    """
    successor = get_nested_value(map_categories_dict, key_path)
    successor_keys = None
    if type(successor) == dict:
        successor_keys = successor.keys()
    elif type(successor) == list:
        successor_keys = successor.copy()
    elif successor_keys is None:
        return None

    new_dropdown_children = list()
    for successor_key in successor_keys:
        successor_key_path = key_path.copy()
        successor_key_path.append(successor_key)

        children = create_nested_dropdown(map_categories_dict, successor_key_path)

        if children is None:
            ID, key = successor_key
            new_dropdown_children.append(html.Div(key, id=ID, className='menu-level2'))
        else:
            # children.append(html.Span(successor_key,className='menu-title'))
            children = [html.Span(successor_key, className='menu-level1-title'),
                        html.Div(children, className='menu-level1-content')]
            new_dropdown_children.append(html.Div(id=successor_key,
                                                  children=children, className="menu-level1"))
    return new_dropdown_children


def get_nested_value(d, key_path: list):
    """
    Extracts item of dictionary for a key.
    :param d: dictionary but with exception.
    :param key_path: list of keys contained in map_categories_dict.
    :return: Sub-dictionary, with None as exception.
    """
    if key_path is None: return None
    for key in key_path:
        if type(d) == dict:
            d = d.get(key)
        else:
            return None
    return d


def main_dropdowns(map_categories_dict: dict, key: str):
    """
    Creates a nested DropdownMenu for all attributes rooted at the most outer category in map_categories_dict
    :param map_categories_dict:
    :param key: The most outer key value, type str.
    :return: a column containing a DropdownMenu.
    """
    x = [html.Span(key, className='menu-level0-title'), html.Div(create_nested_dropdown(map_categories_dict, [key]),
                                                                 className='menu-level0-content')]
    return dbc.Col(html.Div(
        id=key,
        children=x,
        className="menu-level0",
    ), style={'margin-right': '45px'})


def find_button_attribute(attributes: tuple, button_id: str):
    sub_attribute = '"Good Job" local'
    for i, attribute in attributes:
        if i == button_id:
            sub_attribute = attribute
    return sub_attribute


# Defines the layout of all most outer DropdownMenus in map_categories_dict
map_tabs_layout = [main_dropdowns(map_categories_dict, key) for key in map_categories_dict]
# Defines the map, which will interact with the callbacks
choropleth_map_layout = dcc.Graph(id="choropleth-map")


# Define callback to update map based on dropdown selection
@callback(
    [Output("choropleth-map", "figure"),
     Output('borough-dropdown', 'value')],
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

    # Get the selected borough from the map click event
    selected_borough = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    return fig, selected_borough

@callback(
    Output('stored_BR_data', 'data'),
    Input('choropleth-map', 'clickData')
)
def update_stored_borough(clickData):
    if clickData:
        borough = clickData['points'][0]['location']
        return [borough]
    return []
