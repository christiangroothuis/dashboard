from dash import dcc, Input, Output, callback, no_update
import plotly.express as px
import pandas as pd
import os
from pathlib import Path
from dash import html, State


data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
df_granular_pas = pd.read_csv(os.path.join(data_directory, 'age_range.csv'))

line_graph_layout = dcc.Graph(id="h_linechart")

from dash import no_update


@callback(
    Output("h_linechart", "figure"),
    Input('shared-data-store-lg', 'data'),
    Input('selected_borough', 'data'),
    prevent_initial_call=True
)
def update_h_linechart(data, selected_borough):
    if data is None or not data or selected_borough is None:
        return no_update

    df_filtered = pd.DataFrame(data)
    print("Initial DataFrame:", df_filtered.head())
    if 'Year' not in df_filtered.columns:
        raise ValueError("DataFrame does not contain 'Year' column!!")

    # Filter data based on selected boroughs
    if selected_borough:
        df_filtered = df_filtered[df_filtered['Borough'].isin(selected_borough)]

    # Check if 'Year' column exists in the filtered DataFrame
    if 'Year' not in df_filtered.columns:
        raise ValueError("DataFrame does not contain 'Year' column.")

    df_filtered['Count'] = df_filtered.drop(columns=['Borough']).sum(axis=1)
    df_filtered = df_filtered[['Year', 'Borough', 'Count']]
    print(df_filtered.head())

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

from dash import callback, Input, Output, dcc

#@callback(
    #Output('your-output-component-id', 'children'),
    #Input('selected-attribute-store', 'data')
#)
#def use_selected_attribute(selected_attribute):
    #if selected_attribute:
        #return f'The selected attribute is: {selected_attribute}'
    #return 'No attribute selected'


tooltip_layout = html.Div(
    [
        html.Button(
            "?",
            id="tooltip-target",
            style={
                "font-size": "20px",
                "padding": "10px",
                "backgroundColor": "white",
                "color": "black",
                "border": "black",
                "border-radius": "50%",
                "margin-bottom": "10px",
            },
        ),
        html.Div(
            "This graph shows the number of selected responses over time for different boroughs.",
            id="tooltip",
            style={
                "visibility": "hidden",
                "background-color": "black",
                "color": "#fff",
                "text-align": "center",
                "border-radius": "6px",
                "padding": "5px",
                "position": "absolute",
                "z-index": "1",
                "width": "20%",
                "display": "inline-block",
                "verticalAlign": "top",
                "padding": "20px",
                "position": "relative",
            },
        ),
    ]
)


# Callback to show/hide tooltip
@callback(
    Output('tooltip', 'style'),
    Input('tooltip-target', 'n_clicks'),
    State('tooltip', 'style')
)
def toggle_tooltip(n_clicks, style):
    if n_clicks and style['visibility'] == 'hidden':
        style['visibility'] = 'visible'
    else:
        style['visibility'] = 'hidden'
    return style
