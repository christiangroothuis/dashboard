import dash_bootstrap_components as dbc
import dash
from dash import html
from .scripts.map_categories import map_categories_dict
from dash_iconify import DashIconify

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
    ))


# Defines the layout of all most outer DropdownMenus in map_categories_dict
map_tabs_layout = [main_dropdowns(map_categories_dict, key) for key in map_categories_dict]
