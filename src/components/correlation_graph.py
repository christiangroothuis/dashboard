# Imports
from dash import Dash, dcc, html, Input, Output, callback
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
# @callback(
#     Output("correlation-graph", "figure"),
#     [Input(str(i), "n_clicks") for i in range(10)]
# )
# def update_correlation_graph(*args):
#     fig = px.scatter(df_scatter_trend,
#                      x='CrimeRate',
#                      y='ResponseTime',
#                      color='Borough',
#                      trendline='ols',
#                      title='Correlation Between Crime Rate and Police Response Time')
#     fig.update_layout()
#
#     return fig



#Test 2



# @callback(
#     Output("correlation-graph", "figure"),
#     Input('stored_BR_data', 'data')
# )
# def update_correlation_graph(stored_BR_data):
#     if not stored_BR_data:
#         df_filtered = df_scatter_trend
#     else:
#         df_filtered = df_scatter_trend[df_scatter_trend['Borough'].isin(stored_BR_data)]
#
#     fig = px.scatter(
#         df_filtered,
#         x='CrimeRate',
#         y='ResponseTime',
#         color='Borough',
#         trendline='ols',
#         title='Correlation Between Crime Rate and Police Response Time'
#     )
#     fig.update_layout()
#     return fig


#Test 3

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
        title='Correlation Between Crime Rate and Police Response Time'
    )
    fig.update_layout()
    return fig
