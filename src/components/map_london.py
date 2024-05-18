from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

# Import preprocessed data
from .scripts.import_data import df_data, geo_data


map_layout = html.Div([
        dcc.Dropdown(
            id='category',
            options=['"Good Job" local', "Contact ward officer", "Informed local", "Listen to concerns",
                     "Relied on to be there", "Treat everyone fairly", "Understand issues", "Trust MPS"],
            value='"Good Job" local',
        ),
        dcc.Graph(id="map"),
    ])


@callback(
    Output("map", "figure"),
    Input("category", "value"))
def display_choropleth(category):
    fig = px.choropleth(
        data_frame=df_data, geojson=geo_data, locations="Borough", featureidkey="properties.name",
        color=category, color_continuous_scale='viridis',
        projection="mercator")  # equirectangular, mercator
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40})
    return fig