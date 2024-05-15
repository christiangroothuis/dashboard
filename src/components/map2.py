# Imports
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px


# Example data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

print(df)

map_layout2 = html.Div([
    html.H4('Political candidate voting pool analysis'),
    html.P("Select a candidate:"),
    dcc.RadioItems(
        id='candidate',
        options=["Joly", "Coderre", "Bergeron"],
        value="Coderre",
        inline=True
    ),
    dcc.Graph(id="graph")
], style={'width': '48%', 'display': 'block'})


# -------------------------------------------------------------
# Callbacks to update the map depending on chosen attribute
# -------------------------------------------------------------
@callback(
    Output("graph", "figure"),
    [Input("candidate", "value")])
def display_choropleth(candidate):
    # Load election data from Plotly Express
    election_data = px.data.election()

    # Load election GeoJSON data from Plotly Express
    election_geojson = px.data.election_geojson()

    # Filter the election data for the selected candidate
    candidate_data = election_data[election_data['district'] == candidate]

    # Merge the filtered data with the GeoJSON data
    merged_data = election_geojson.merge(candidate_data, on='district', how='left')

    # Create choropleth map figure
    fig = px.choropleth(
        merged_data, geojson=merged_data.geometry, color=candidate,
        locations=merged_data.index, projection="mercator", range_color=[0, 6500])

    # Update map layout
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig