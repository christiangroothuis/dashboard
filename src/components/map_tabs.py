import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State, callback_context, dcc
import plotly.express as px
import os
from pathlib import Path
import pandas as pd

from .scripts.map_categories import map_categories_dict
from .scripts.geo_borough import import_geo_borough_data

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')

# Import all data
geo_data, _ = import_geo_borough_data(data_directory, 'geo_boroughs.geojson')
df_pas_original = pd.read_csv(os.path.join(data_directory, 'pas_original.csv'))
df_pas_granular = pd.read_csv(os.path.join(data_directory, 'pas_granular.csv'))
df_outcomes = pd.read_csv(os.path.join(data_directory, 'outcomes.csv'))
df_stop_search = pd.read_csv(os.path.join(data_directory, 'stop_search.csv'))
df_street = pd.read_csv(os.path.join(data_directory, 'street.csv'))
df_economic = pd.read_csv(os.path.join(data_directory, 'economic.csv'))
df_ethnicity = pd.read_csv(os.path.join(data_directory, 'ethnicity.csv'))


def reformat_crime_data(dataframe, columns_name):
    df = pd.DataFrame(dataframe.copy().groupby(['Borough', 'Year', columns_name]).size().reset_index(name='Count'))
    df = df.pivot_table(index=['Borough', 'Year'], columns=columns_name, values='Count', fill_value=0).reset_index()
    print(df)
    return df


df_outcomes = reformat_crime_data(df_outcomes, 'Outcome Type')
df_age_rage = reformat_crime_data(df_stop_search, 'Age Range')
df_officer_def_ethnicity = reformat_crime_data(df_stop_search, 'Officer Def Ethinicty')
df_legislation = reformat_crime_data(df_stop_search, 'Legislation')
df_search_object = reformat_crime_data(df_stop_search, 'Search Object')
df_ss_outcome = reformat_crime_data(df_stop_search, 'Outcome')
df_crime_type = reformat_crime_data(df_street, 'Crime Type')
df_last_outcome = reformat_crime_data(df_street, 'Last Out Cat')


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


# =====================
#      Callbacks
# =====================
# Define callback to update map based on dropdown selection
@callback(
    [Output("choropleth-map", "figure"),
     Output('borough-dropdown', 'value')],
    [Input(str(i), "n_clicks") for i in range(0, 133)]
)
def update_map(*args):
    """
    Updates the choropleth plot based on the nested dropdown.
    :param args: the IDs of all selectable categories in the nested drop-downs.
    :return: choropleth plot.
    """

    global sub_attribute
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    print('button_id', button_id)

    df_data = pd.DataFrame()

    # Find out what attribute should be displayed in plot depending on IDs of type str(int).
    if button_id is None:
        df_data = df_pas_original
        sub_attribute = '"Good Job" local'  # Default to Trust_score if no button is clicked

    # PAS
    elif 0 <= int(button_id) <= 9:
        df_data = df_pas_original.copy()
        print(df_data)
        if 0 <= int(button_id) <= 4:
            attributes = map_categories_dict['PAS']['Confidence']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 5 <= int(button_id) <= 7:
            attributes = map_categories_dict['PAS']['Trust']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 8 <= int(button_id) <= 9:
            attributes = map_categories_dict['PAS']['Other']
            sub_attribute = find_button_attribute(attributes, button_id)

    # Economic and Ethnicity
    elif 115 <= int(button_id) <= 132:
        if 115 <= int(button_id) <= 119:
            df_data = df_ethnicity.copy()
            attributes = map_categories_dict['Economic']['Demographic']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 120 <= int(button_id) <= 126:
            df_data = df_economic.copy()
            attributes = map_categories_dict['Economic']['Industry types']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 127 <= int(button_id) <= 132:
            df_data = df_economic.copy()
            attributes = map_categories_dict['Economic']['Employment']
            sub_attribute = find_button_attribute(attributes, button_id)

    # Stop&Search
    elif 32 <= int(button_id) <= 73:
        if 32 <= int(button_id) <= 37:
            df_data = df_age_rage.copy()
            attributes = map_categories_dict['Stop&Search']['Age Range']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 38 <= int(button_id) <= 42:
            df_data = df_officer_def_ethnicity.copy()
            attributes = map_categories_dict['Stop&Search']['Officer Defined Ethnicity']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 43 <= int(button_id) <= 48:
            df_data = df_legislation.copy()
            attributes = map_categories_dict['Stop&Search']['Legislation']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 49 <= int(button_id) <= 57:
            df_data = df_search_object.copy()
            attributes = map_categories_dict['Stop&Search']['Search Object']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 58 <= int(button_id) <= 73:
            df_data = df_ss_outcome.copy()
            attributes = map_categories_dict['Stop&Search']['Stop and Search Outcome']
            sub_attribute = find_button_attribute(attributes, button_id)

    # StreetCrime
    elif 74 <= int(button_id) <= 113:
        if 74 <= int(button_id) <= 88:
            df_data = df_crime_type.copy()
            attributes = map_categories_dict['StreetCrime']['Crime Type Street']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 89 <= int(button_id) <= 113:
            df_data = df_last_outcome.copy()
            attributes = map_categories_dict['StreetCrime']['Last Outcome']
            sub_attribute = find_button_attribute(attributes, button_id)

    # Outcomes
    elif 10 <= int(button_id) <= 31:
        print('HELLO')
        print(df_outcomes)
        df_data = df_outcomes.copy()
        print(df_data)

        attributes = map_categories_dict['CrimeOutcomes']
        sub_attribute = find_button_attribute(attributes, button_id)
        print(sub_attribute)

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
    Input('choropleth-map', 'clickData'),
    State('stored_BR_data', 'data')  # Add State to get current data
)
def update_stored_borough(clickData, stored_data):
    if stored_data is None:  # Handle the case when there is no initial data
        stored_data = []

    if clickData:
        borough = clickData['points'][0]['location']
        if borough not in stored_data:
            stored_data.append(borough)

    return stored_data
