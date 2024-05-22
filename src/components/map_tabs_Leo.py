import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    'Region': ['Region1', 'Region2', 'Region3'],
    'Trust_score': [0.6, 0.7, 0.5],
    'Confidence_score': [0.8, 0.65, 0.78],
    'Crime_rate': [0.3, 0.4, 0.6],
    'Economy_score': [0.5, 0.6, 0.7],
    'lat': [51.5, 51.6, 51.7],
    'lon': [-0.1, -0.2, -0.3]
})

# Create the layout
map_tabs_layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.DropdownMenu(
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
        ), width="auto"),
        dbc.Col(dbc.DropdownMenu(
            label="Crime Rate",
            children=[
                dbc.DropdownMenuItem("Crime Rate", id="crime-rate"),
                dbc.DropdownMenuItem("Crime Capture Rate", id="crime-capture-rate"),
            ],
            direction="down",
            className="me-1"
        ), width="auto"),
        dbc.Col(dbc.DropdownMenu(
            label="Economy",
            children=[
                dbc.DropdownMenuItem("Economy Score", id="economy-score"),
                dbc.DropdownMenuItem("GDP", id="gdp"),
            ],
            direction="down",
            className="me-1"
        ), width="auto"),
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="choropleth-map"), width=12)
    ])
], fluid=True)


# Define callback to update map based on dropdown selection
@callback(
    Output("choropleth-map", "figure"),
    [Input("trust-score", "n_clicks"),
     Input("response-time", "n_clicks"),
     Input("confidence-score", "n_clicks"),
     Input("public-opinion", "n_clicks"),
     Input("crime-rate", "n_clicks"),
     Input("crime-capture-rate", "n_clicks"),
     Input("economy-score", "n_clicks"),
     Input("gdp", "n_clicks")]
)
def update_map(trust_clicks, response_time_clicks, confidence_clicks, public_opinion_clicks,
               crime_rate_clicks, crime_capture_rate_clicks, economy_score_clicks, gdp_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if button_id == "trust-score":
        sub_attribute = "Trust_score"
    elif button_id == "response-time":
        sub_attribute = "Response_time"
    elif button_id == "confidence-score":
        sub_attribute = "Confidence_score"
    elif button_id == "public-opinion":
        sub_attribute = "Public_opinion"
    elif button_id == "crime-rate":
        sub_attribute = "Crime_rate"
    elif button_id == "crime-capture-rate":
        sub_attribute = "Crime_capture_rate"
    elif button_id == "economy-score":
        sub_attribute = "Economy_score"
    elif button_id == "gdp":
        sub_attribute = "GDP"
    else:
        sub_attribute = None

    if sub_attribute is None:
        sub_attribute = "Trust_score"  # Default to Trust_score if no button is clicked

    fig = px.choropleth_mapbox(
        df,
        geojson=None,  # Replace with actual GeoJSON data
        locations="Region",
        color=sub_attribute,
        hover_name="Region",
        mapbox_style="carto-positron",
        center={"lat": 51.5074, "lon": -0.1278},
        zoom=10
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig
