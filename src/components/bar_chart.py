# Imports
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd

# Sample data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 1, 5, 3],
    'category': ['A', 'B', 'A', 'B', 'A']
})

barchart_layout = dcc.Graph(
            id='scatter-plot',
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['category'] == category]['x'],
                        y=df[df['category'] == category]['y'],
                        mode='markers',
                        name=category
                    ) for category in df['category'].unique()
                ],
                'layout': go.Layout(
                    title='Scatter Plot',
                    xaxis={'title': 'X-axis'},
                    yaxis={'title': 'Y-axis'},
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                    hovermode='closest'
                )
            }
        )