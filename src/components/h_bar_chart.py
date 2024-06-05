# Imports
from dash import dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
import plotly.graph_objects as go

h_barchart_layout = dcc.Graph(id="h_barchart")

data_directory = os.path.join(Path(os.getcwd()).parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'pas_data_ward_level/PAS_ward_level_FY_20_21.csv'))
df_grouped = df_granular_pas.groupby(['Borough', 'Q1']).size().unstack().fillna(0)


#Test 3

# @callback(
#     Output("h_barchart", "figure"),
#     Input('selected_borough', 'data'),
#     prevent_initial_call=True
# )
# def update_h_barchart(selected_borough):
#     if not selected_borough:
#         df_filtered = df_grouped.sum(axis=1).reset_index()
#     else:
#         df_filtered = df_grouped.loc[selected_borough].sum(axis=1).reset_index()
#
#     fig = px.bar(
#         df_filtered,
#         y='Borough',
#         x=0,
#         labels={'0': 'Count', 'Borough': 'Borough'},
#         title='Distribution of trust in neighbourhood per borough'
#     )
#     fig.update_layout(
#         barmode='stack',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         height=600  # Set a specific height for consistency
#     )
#     fig.update_layout(barmode='stack')
#     return fig

# @callback(
#     Output("h_barchart", "figure"),
#     Input('selected_borough', 'data'),
#     prevent_initial_call=True
# )
# def update_h_barchart(selected_borough):
#     if not selected_borough:
#         df_filtered = df_grouped.sum(axis=1).reset_index()
#     else:
#         df_filtered = df_grouped.loc[selected_borough].sum(axis=1).reset_index()
#
#     fig = px.bar(
#         df_filtered,
#         y='Borough',
#         x=0,
#         labels={'0': 'Count', 'Borough': 'Borough'},
#         title='Distribution of trust in neighbourhood per borough'
#     )
#
#     # Conditionally color the bars based on selection
#     fig.update_traces(marker_color='lightgrey', selector=dict(type='bar'))
#     if selected_borough:
#         fig.update_traces(marker_color='blue', selector=dict(type='bar', name='Selected Boroughs'))
#
#     fig.update_layout(
#         barmode='stack',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         height=600  # Set a specific height for consistency
#     )
#     return fig


# @callback(
#     Output("h_barchart", "figure"),
#     Input('selected_borough', 'data'),
#     prevent_initial_call=True
# )
# def update_h_barchart(selected_borough):
#     if not selected_borough:
#         df_filtered = df_grouped.sum(axis=1).reset_index()
#     else:
#         df_filtered = df_grouped.loc[selected_borough].sum(axis=1).reset_index()
#         # Reorder DataFrame based on selected boroughs
#         df_filtered = df_filtered.sort_values(by=0, ascending=False)
#         selected_borough = df_filtered['Borough'].tolist()  # Update selected_borough to reflect new order
#
#     fig = px.bar(
#         df_filtered,
#         y='Borough',
#         x=0,
#         labels={'0': 'Count', 'Borough': 'Borough'},
#         title='Distribution of trust in neighbourhood per borough'
#     )
#
#     # Conditionally color the bars based on selection
#     fig.update_traces(marker_color='lightgrey', selector=dict(type='bar'))
#     if selected_borough:
#         fig.update_traces(marker_color='blue', selector=dict(type='bar', name='Selected Boroughs'))
#
#     fig.update_layout(
#         barmode='stack',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         height=600  # Set a specific height for consistency
#     )
#     return fig


@callback(
    Output("h_barchart", "figure"),
    Input('selected_borough', 'data'),
    prevent_initial_call=True
)
def update_h_barchart(selected_borough):
    if not selected_borough:
        df_filtered = df_grouped.sum(axis=1).reset_index()
        colors = ['lightgrey'] * len(df_filtered)
    else:
        df_filtered = df_grouped.sum(axis=1).reset_index()
        colors = ['blue' if borough in selected_borough else 'lightgrey' for borough in df_filtered['Borough']]

    fig = go.Figure(
        data=[go.Bar(
            y=df_filtered['Borough'],
            x=df_filtered[0],
            marker_color=colors,  # Set marker color based on the colors list
            text=df_filtered[0],
            orientation='h'
        )]
    )

    fig.update_layout(
        title='Distribution of trust in neighbourhood per borough',
        yaxis=dict(title='Borough'),
        xaxis=dict(title='Count'),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=600  # Set a specific height for consistency
    )

    return fig

