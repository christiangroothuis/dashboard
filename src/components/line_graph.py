from dash import dcc, Input, Output, callback, no_update
import plotly.express as px
import pandas as pd
import os
from pathlib import Path


data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'age_range.csv'))

line_graph_layout = dcc.Graph(id="h_linechart")

from dash import no_update


@callback(
    Output("h_linechart", "figure"),
    Input('shared-data-store', 'data'),
    Input('selected_borough', 'data'),
    prevent_initial_call=True
)
def update_h_linechart(data, selected_borough):
    if data is None or not data or selected_borough is None:
        return no_update

    df_filtered = pd.DataFrame(data)

    # Filter data based on selected boroughs
    if selected_borough:
        df_filtered = df_filtered[df_filtered['Borough'].isin(selected_borough)]

    # Check if 'Year' column exists in the filtered DataFrame
    if 'Year' not in df_filtered.columns:
        raise ValueError("DataFrame does not contain 'Year' column.")

    # Assuming '10-17' column exists in df_filtered
    fig = px.line(
        df_filtered,
        x='Year',
        y='10-17',  # Update to the column name you want on the y-axis
        color='Borough',  # Color lines by Borough
        labels={'Year': 'Year', '10-17': '10-17 Count'},  # Update labels as needed
    )
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=600,  # Set a specific height for consistency
        xaxis_title='Year'  # Set x-axis title
    )

    return fig
