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
        successor_key_path = key_path.copy()
        successor_key_path.append(successor_key)

        children = create_nested_dropdown(map_categories_dict, successor_key_path)

        if children is None:
            ID, key = successor_key
            new_dropdown_children.append(dbc.DropdownMenuItem(key, id=ID))
        else:
            new_dropdown_children.append(dbc.DropdownMenu(label=successor_key, id=successor_key, children=children))
    return new_dropdown_children


def main_dropdowns(map_categories_dict, key):

    children = create_nested_dropdown(map_categories_dict, [key])

    return dbc.Col(dbc.DropdownMenu(
        label=key,
        id=key,
        children=create_nested_dropdown(map_categories_dict, [key]),
        direction="down",
        className="me-1"
    ), width="auto")


map_tabs_layout = [main_dropdowns(map_categories_dict, key) for key in map_categories_dict]
