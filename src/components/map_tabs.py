import dash_bootstrap_components as dbc
from .scripts.map_categories import map_categories_dict


def get_nested_value(d, key_path):
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


def create_nested_dropdown(map_categories_dict, key_path):
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
            new_dropdown_children.append(dbc.DropdownMenuItem(key, id=ID))
        else:
            new_dropdown_children.append(dbc.DropdownMenu(label=successor_key, id=successor_key, children=children))
    return new_dropdown_children


def main_dropdowns(map_categories_dict, key):
    """
    Creates a nested DropdownMenu for all attributes rooted at the most outer category in map_categories_dict
    :param map_categories_dict:
    :param key: The most outer key value, type str.
    :return: a column containing a DropdownMenu.
    """

    return dbc.Col(dbc.DropdownMenu(
        label=key,
        id=key,
        children=create_nested_dropdown(map_categories_dict, [key]),
        direction="down",
        className="me-1"
    ), width="auto")


# Defines the layout of all most outer DropdownMenus in map_categories_dict
map_tabs_layout = [main_dropdowns(map_categories_dict, key) for key in map_categories_dict]
