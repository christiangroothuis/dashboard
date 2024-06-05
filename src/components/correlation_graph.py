# Imports
from dash import dcc, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px


correlation_graph_layout = dcc.Graph(id="correlation-graph")


# Sample data for scatter plot with trendline
scatter_trend_data = {
    'Borough': ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley'] * 10,
    'CrimeRate': np.random.normal(60, 10, 50),
    'ResponseTime': np.random.normal(30, 5, 50)
}
df_scatter_trend = pd.DataFrame(scatter_trend_data)

@callback(
    Output("correlation-graph", "figure"),
    Input('stored_BR_data', 'data'),
    prevent_initial_call=True
)
def update_correlation_graph(selected_boroughs):
    if not selected_boroughs:
        df_filtered = df_scatter_trend
    else:
        df_filtered = df_scatter_trend[df_scatter_trend['Borough'].isin(selected_boroughs)]

    fig = px.scatter(
        df_filtered,
        x='CrimeRate',
        y='ResponseTime',
        color='Borough',
        trendline='ols',

    )
    # Update layout to set background to clear
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=600  # Set a specific height for consistency
    )
    fig.update_layout()
    return fig
