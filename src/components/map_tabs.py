import dash_bootstrap_components as dbc
from .scripts.map_categories import map_categories_dict


def get_nested_value(d, key_path):
    if key_path is None: return None
    for key in key_path:
        if type(d) == dict:
            d = d.get(key)
        else:
            return None
    return d


def create_nested_dropdown(map_categories_dict, key_path):
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
        print('successor_key', successor_key)
        successor_key_path = key_path.copy()
        successor_key_path.append(successor_key)

        children = create_nested_dropdown(map_categories_dict, successor_key_path)

        if children is None:
            new_dropdown_children.append(dbc.DropdownMenuItem(successor_key, id=successor_key))
        else:
            print('children not none!')
            print(children)
            print(type(children))
            print(len(children))

            new_dropdown_children.append(dbc.DropdownMenu(label=successor_key, id=successor_key, children=children))
            print('children not none POST!')
    return new_dropdown_children


def main_dropdowns(map_categories_dict, key):

    children = create_nested_dropdown(map_categories_dict, [key])
    print('hello', children)

    return dbc.Col(dbc.DropdownMenu(
        label=key,
        id=key,
        children=create_nested_dropdown(map_categories_dict, [key]),
        direction="down",
        className="me-1"
    ), width="auto")


map_tabs_layout = [main_dropdowns(map_categories_dict, key) for key in map_categories_dict]

"""map_tabs_layout = [dbc.Col(dbc.DropdownMenu(
    label="Trust",
    children=[
        dbc.DropdownMenuItem("Trust Score", id="trust-score"),
        dbc.DropdownMenuItem("Response Time", id="response-time"),
    ],
    direction="down",
    className="me-1"
), width="auto"),
    dbc.Col(dbc.DropdownMenu(
        label="Confidence",
        children=[
            dbc.DropdownMenuItem("Confidence Score", id="confidence-score"),
            dbc.DropdownMenuItem("Public Opinion", id="public-opinion"),
        ],
        direction="down",
        className="me-1"
    ), width="auto")]"""
