from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc


dropdown_menu = dbc.DropdownMenu(
    label="Dropdown button",
    children=[
        dbc.DropdownMenuItem("Action", href="#"),
        dbc.DropdownMenuItem("Another action", href="#"),
        dbc.DropdownMenuItem(
            [
                "Submenu »",
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Submenu item 1", href="#"),
                        dbc.DropdownMenuItem("Submenu item 2", href="#"),
                        dbc.DropdownMenuItem(
                            [
                                "Submenu item 3 »",
                                dbc.DropdownMenu(
                                    [
                                        dbc.DropdownMenuItem("Multi level 1", href="#"),
                                        dbc.DropdownMenuItem("Multi level 2", href="#")
                                    ],
                                    in_navbar=True,
                                    label="",
                                    right=True,
                                ),
                            ],
                            header=True,
                        ),
                        dbc.DropdownMenuItem("Submenu item 4", href="#"),
                        dbc.DropdownMenuItem("Submenu item 5", href="#")
                    ],
                    in_navbar=True,
                    label="",
                    right=True,
                ),
            ],
            header=True,
        ),
    ],
)