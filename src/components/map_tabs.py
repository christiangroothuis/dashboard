import dash_bootstrap_components as dbc
import dash
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
df_pas_questions = pd.read_csv(os.path.join(data_directory, 'pas_proportions_test.csv'))

df_outcomes = pd.read_csv(os.path.join(data_directory, 'outcomes_pivot.csv')).drop(columns='Unnamed: 0')
df_age_rage = pd.read_csv(os.path.join(data_directory, 'age_range.csv')).drop(columns='Unnamed: 0')
df_officer_def_ethnicity = pd.read_csv(os.path.join(data_directory, 'officer_def_ethnicity.csv')).drop(columns='Unnamed: 0')
df_legislation = pd.read_csv(os.path.join(data_directory, 'legislation.csv')).drop(columns='Unnamed: 0')
df_search_object = pd.read_csv(os.path.join(data_directory, 'search_object.csv')).drop(columns='Unnamed: 0')
df_ss_outcome = pd.read_csv(os.path.join(data_directory, 'ss_outcome.csv')).drop(columns='Unnamed: 0')
df_crime_type = pd.read_csv(os.path.join(data_directory, 'crime_type.csv')).drop(columns='Unnamed: 0')
df_last_outcome = pd.read_csv(os.path.join(data_directory, 'ss_last_outcome.csv')).drop(columns='Unnamed: 0')

df_economic = pd.read_csv(os.path.join(data_directory, 'economic.csv'))
df_ethnicity = pd.read_csv(os.path.join(data_directory, 'ethnicity.csv'))

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
            new_dropdown_children.append(html.Div(f'→ {key}', id=ID, className='menu-level2'))
        else:
            # children.append(html.Span(successor_key,className='menu-title'))
            children = [html.Span(f'▶ {successor_key}', className='menu-level1-title'),
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

button_to_borough = {str(i): borough for i, borough in enumerate(df_pas_original['Borough'].unique())}
attribute_click_counts = {str(i): 0 for i in range(0, 165)}
previously_clicked_attribute = 0

# =====================
#      Callbacks
# =====================
# Define callback to update map based on dropdown selection
@callback(
    Output("choropleth-map", "figure"),
    [*[Input(str(i), "n_clicks") for i in range(0, 151)],
     Input('range-slider', 'value')],
)
def update_map(*args):
    """
    Updates the choropleth plot based on the nested dropdown.
    :param args: the IDs of all selectable categories in the nested drop-downs.
    :return: choropleth plot.
    """
    global sub_attribute
    global attribute_click_counts, previously_clicked_attribute

    # Extract the number of clicks for each attribute selection
    attribute_clicks = args[:151]
    attribute_clicks = [click if click is not None else 0 for click in attribute_clicks]

    # Extract the selected time interval
    year_range = args[151]

    # Determine which attribute was clicked most recently
    most_recently_clicked = None
    for i in range(0, 151):
        if attribute_clicks[i] > attribute_click_counts[str(i)]:
            most_recently_clicked = i
            previously_clicked_attribute = most_recently_clicked
            attribute_click_counts[str(i)] = attribute_clicks[i]

    button_id = str(previously_clicked_attribute)
    print('Start button_id: ', button_id)
    df_data = pd.DataFrame()

    pas_granular_bool = False

    # Find out what attribute should be displayed in plot depending on IDs of type str(int).
    if button_id is None:
        df_data = df_pas_original
        sub_attribute = '"Good Job" local'  # Default to Trust_score if no button is clicked

    # PAS
    elif 0 <= int(button_id) <= 37:
        if 0 <= int(button_id) <= 4:
            df_data = df_pas_original.copy()
            attributes = map_categories_dict['PAS']['Confidence']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 5 <= int(button_id) <= 7:
            df_data = df_pas_original.copy()
            attributes = map_categories_dict['PAS']['Trust']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 8 <= int(button_id) <= 9:
            df_data = df_pas_original.copy()
            attributes = map_categories_dict['PAS']['Other']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 10 <= int(button_id) <= 37:
            pas_granular_bool = True
            df_data = df_pas_questions.copy()
            attributes = map_categories_dict['PAS']['PAS-Granular']
            sub_attribute = find_button_attribute(attributes, button_id)

    # Economic and Ethnicity
    elif 38 <= int(button_id) <= 55:
        if 38 <= int(button_id) <= 42:
            df_data = df_ethnicity.copy()
            attributes = map_categories_dict['Economic']['Demographic']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 43 <= int(button_id) <= 49:
            df_data = df_economic.copy()
            attributes = map_categories_dict['Economic']['Industry types']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 50 <= int(button_id) <= 55:
            df_data = df_economic.copy()
            attributes = map_categories_dict['Economic']['Employment']
            sub_attribute = find_button_attribute(attributes, button_id)

    # Stop&Search
    elif 56 <= int(button_id) <= 92:
        if 56 <= int(button_id) <= 60:
            df_data = df_age_rage.copy()
            attributes = map_categories_dict['Stop&Search']['Age Range']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 61 <= int(button_id) <= 64:
            df_data = df_officer_def_ethnicity.copy()
            attributes = map_categories_dict['Stop&Search']['Officer Defined Ethnicity']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 65 <= int(button_id) <= 69:
            df_data = df_legislation.copy()
            attributes = map_categories_dict['Stop&Search']['Legislation']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 70 <= int(button_id) <= 77:
            df_data = df_search_object.copy()
            attributes = map_categories_dict['Stop&Search']['Search Object']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 78 <= int(button_id) <= 92:
            df_data = df_ss_outcome.copy()
            attributes = map_categories_dict['Stop&Search']['Stop and Search Outcome']
            sub_attribute = find_button_attribute(attributes, button_id)

    # StreetCrime
    elif 93 <= int(button_id) <= 130:
        if 93 <= int(button_id) <= 106:
            df_data = df_crime_type.copy()
            attributes = map_categories_dict['StreetCrime']['Crime Type Street']
            sub_attribute = find_button_attribute(attributes, button_id)
        elif 107 <= int(button_id) <= 130:
            df_data = df_last_outcome.copy()
            attributes = map_categories_dict['StreetCrime']['Last Outcome']
            sub_attribute = find_button_attribute(attributes, button_id)

    # Outcomes
    elif 131 <= int(button_id) <= 150:
        df_data = df_outcomes.copy()
        attributes = map_categories_dict['CrimeOutcomes']
        sub_attribute = find_button_attribute(attributes, button_id)

    else:
        sub_attribute = None

    if sub_attribute is None:
        sub_attribute = '"Good Job" local'  # Default to Trust_score if no button is clicked

    start_year, end_year = year_range
    df_data = df_data[df_data['Year'].between(start_year-1, end_year)]

    if pas_granular_bool:
        # list of question columns
        questions_names = ['SS Agree', 'SS Fair', 'Crime Victim', 'Officer Contact', 'Met Trust',
        'Police Accountable', 'Met Career', 'Gangs', 'Law Obligation', 'Area Living Time',
        'Crime Local Worry', 'Informed Local', 'Informed London', 'Asb Worry', 'Guns',
        'Knife Crime', 'People Trusted', 'People Courtesy', 'People Help', 'Call Suspicious',
        'Different Backgrounds', 'Good Job Local', 'Good Job London', 'Police Reliance',
        'Police Respect', 'Police Fair Treat', 'Community Matter', 'Local Concerns']

        def remove_prefix_suffix(s, prefix):
            s = s.rsplit(' ', 1)[0]
            result = s.removeprefix(prefix + ' ')
            return result

        for prefix in questions_names:
            cols = [col for col in df_data.columns if col.startswith(prefix)]
            # Create hover text
            df_data[f'Proportions {prefix}<br>'] = df_data[cols].apply(
                lambda row: '<br>'.join([f'{col}: {row[col]:.2f}' for col in df_data.columns if col.startswith(prefix)]) , axis=1)
            # Get the mode
            df_data[f'{prefix}_mode_initial'] = df_data[cols].idxmax(axis=1)
            df_data[prefix] = df_data[f'{prefix}_mode_initial'].apply(remove_prefix_suffix, prefix=prefix)
            # Remove irrelevant column
            col_name = f'{prefix}_mode_initial'
            if col_name in df_data.columns:
                df_data.drop(columns=col_name, inplace=True)

        fig = px.choropleth(
        data_frame=df_data, geojson=geo_data, locations="Borough", featureidkey="properties.name",
        color=sub_attribute, hover_data={f'Proportions {sub_attribute}<br>': True},
        color_discrete_sequence=px.colors.qualitative.D3, projection="mercator")

    else:
        df_data = df_data.drop(columns='Year').groupby('Borough').sum().reset_index()

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
