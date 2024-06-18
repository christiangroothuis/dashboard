import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback

# Mapping for attribute-tt values to tooltip texts
attribute_tooltips = {
    'PAS-Confidence': 'omg PAS',
    'PAS-Trust': 'what wowie trust?!',
    # Add more mappings as needed
}

# Tooltip component
tooltip_layout = html.Div(
    [
        html.P(
            [
                "Want to know more about the selected category and the included attributes?",
                html.Span(
                    " Click here!",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),
            ],
            style={"textAlign": "center", "fontStyle": "italic"}   # Center the text, Make the text italic
        ),
        dbc.Tooltip(
            id="tooltip",  # Unique ID for the tooltip
            target="tooltip-target",
            children="Noun: rare, the action or habit of estimating something as worthless.",
        ),
    ]
)

# Callback to update the tooltip text based on 'attribute-tt'
@callback(
    Output('tooltip', 'children'),
    Input('attribute-tt', 'data')
)
def update_tooltip_text(data):
    return attribute_tooltips.get(data, "Noun: rare, the action or habit of estimating something as worthless.")