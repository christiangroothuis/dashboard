from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import pandas as pd
import os
from pathlib import Path


# from .scripts.import_data import df_pas_granular as df

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
df = pd.read_csv(os.path.join(data_directory, 'pas_granular.csv'))


# Load and preprocess the data
columns_to_keep = ['Year', 'Borough', 'Ss Agree Neither Agree Nor Disagree']


# Create a list of unique responses, filtering out any null values
responses = df['Ss Agree Neither Agree Nor Disagree'].dropna().unique()

# Create the initial plot with all boroughs, taking 'Fairly worried' as a default
default_response = 'Fairly worried'
filtered_df = df[df['Ss Agree Neither Agree Nor Disagree'] == default_response]
count_by_month_borough = filtered_df.groupby(['Year', 'Borough']).size().reset_index(name='Count')
boroughs = count_by_month_borough['Borough'].unique()

fig = go.Figure()
for borough in boroughs:
    df_borough = count_by_month_borough[count_by_month_borough['Borough'] == borough]
    fig.add_trace(go.Scatter(x=df_borough['Year'], y=df_borough['Count'], mode='lines+markers', name=borough))

buttons = []
for borough in boroughs:
    buttons.append(dict(method='update',
                        label=borough,
                        args=[{'visible': [borough == b for b in boroughs]},
                              {'title': f'Number of "{default_response}" responses over time in {borough}'}]))

buttons.append(dict(method='update',
                    label='All',
                    args=[{'visible': [True] * len(boroughs)},
                          {'title': f'Number of "{default_response}" responses over time by Borough'}]))

fig.update_layout(
    updatemenus=[dict(active=0,
                      buttons=buttons,
                      x=1.1,
                      y=1.15,
                      xanchor='right',
                      yanchor='top')],
    xaxis_title='Month',
    yaxis_title='Count',
    xaxis=dict(tickangle=45),
    template='plotly_white'
)

# Layout for the Dash app
line_graph_layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='response-dropdown',
            options=[{'label': response, 'value': response} for response in responses],
            value=default_response,
            clearable=False,
            style={"margin-bottom": "20px"},
        ),
        dcc.Dropdown(
            id='borough-dropdown',
            options=[{'label': borough, 'value': borough} for borough in boroughs],
            value=[boroughs],
            multi=True,
            style={"margin-bottom": "20px"},
        ),
        dcc.Graph(id='line-chart', figure=fig),
    ], style={"width": "75%", "display": "inline-block", "padding": "20px"}),

    html.Div([
        html.Button("?", id="tooltip-target",
                    style={"font-size": "20px", "padding": "10px", "backgroundColor": "white", "color": "black",
                           "border": "black", "border-radius": "50%", "margin-bottom": "10px"}),
        html.Div("This graph shows the number of selected responses over time for different boroughs.",
                 id="tooltip",
                 style={"visibility": "hidden",
                        "background-color": "black",
                        "color": "#fff",
                        "text-align": "center",
                        "border-radius": "6px",
                        "padding": "5px",
                        "position": "absolute",
                        "z-index": "1"}),
    ], style={"width": "20%", "display": "inline-block", "verticalAlign": "top", "padding": "20px",
              "position": "relative"})
], style={"display": "flex", "justifyContent": "space-around"}
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



@callback(
    Output('line-chart', 'figure'),
    [Input('response-dropdown', 'value'),
     Input('selected_borough', 'data')]
)
def update_graph(selected_response, selected_borough):
    if selected_response is None:
        return go.Figure()

    if not selected_borough:
        selected_boroughs = df['Borough'].unique()

    filtered_df = df[df['Q13'] == selected_response]
    count_by_month_borough = filtered_df.groupby(['Year', 'Borough']).size().reset_index(name='Count')

    fig = go.Figure()

    for borough in selected_borough:
        df_borough = count_by_month_borough[count_by_month_borough['Borough'] == borough]
        fig.add_trace(go.Scatter(x=df_borough['Year'], y=df_borough['Count'], mode='lines+markers', name=borough))

    fig.update_layout(
        title=f'Number of "{selected_response}" responses over time',
        xaxis_title='Month',
        yaxis_title='Count',
        xaxis=dict(tickangle=45),
        template='plotly_white'
    )

    return fig