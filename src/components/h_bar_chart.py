# Imports
from dash import dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import os
import dash_bootstrap_components as dbc
from pathlib import Path
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State, callback_context, dcc
import plotly.express as px
#from .scripts.import_data import df_data, geo_data4
from dash.exceptions import PreventUpdate

h_barchart_layout = dcc.Graph(id="h_barchart")

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'pas_data_ward_level/PAS_ward_level_FY_20_21.csv'))
df_grouped = df_granular_pas.groupby(['Borough', 'Q1']).size().unstack().fillna(0)


@callback(
    Output("h_barchart", "figure"),
    Input('selected_borough', 'data'),
    prevent_initial_call=True
)
def update_h_barchart(selected_borough):
    # Sum the counts for each borough across all Q1 responses
    df_filtered = df_grouped.sum(axis=1).reset_index()
    df_filtered.columns = ['Borough', 'Count']

    # Determine color scheme
    if selected_borough:
        df_filtered['selected'] = df_filtered['Borough'].apply(lambda x: x in selected_borough)
        df_filtered = df_filtered.sort_values(by=['selected', 'Count'], ascending=[False, False])

        # Define colors: brighter for selected, darker for others
        colors = ['#636EFA' if sel else '#B5B5B5' for sel in df_filtered['selected']]
        df_filtered = df_filtered.drop(columns=['selected'])
    else:
        df_filtered = df_filtered.sort_values(by='Count', ascending=False)

        # Use a default color palette when no borough is selected
        colors = px.colors.qualitative.Pastel

    # Create the bar chart
    fig = px.bar(
        df_filtered,
        y='Borough',
        x='Count',
        color='Borough',  # Color by Borough to keep unique entries
        color_discrete_sequence=colors if selected_borough else px.colors.qualitative.Pastel,
        # Apply the custom color scheme
    )

    # Update the layout to accept click events
    fig.update_layout(
        clickmode='event+select',  # Enable click events
        showlegend=False,  # Hide legend if not necessary
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=600  # Set a specific height for consistency
    )

    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)

    # Check if a bar was clicked
    ctx = callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']
        if prop_id.startswith("h_barchart") and prop_id.endswith(".clickData"):
            clicked_borough = ctx.triggered[0]['value']['points'][0]['y']
            if clicked_borough not in selected_borough:
                selected_borough.append(clicked_borough)

    return fig


