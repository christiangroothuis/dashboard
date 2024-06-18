import os
from typing import Any
import dash
from dash import Output, Input, State, html, dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import pandas as pd
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.utils import to_time_series_dataset
from tslearn.clustering import TimeSeriesKMeans
import numpy as np
import plotly.graph_objs as go

from .map_tabs import data_directory

from typing import TypedDict
import numpy as np


class Recommendation(TypedDict):
    borough: str
    metric: str
    borough_to_compare: str
    distance: float | np.floating
    pivot_point: str


button = dbc.Button(
    children=[
        DashIconify(icon="ci:hamburger-lg", width=24, height=24, color="#c2c7d0")
    ],
    id="sidebar-button",
    style={"background-color": "white", "border": "none", "margin-left": "15px"},
)

# create joined df of financial and ethical and geo data
dfs_to_join = [
    "pas_original_aggregated.csv",
    "ethnicity.csv",
    "economic.csv",
]

cluster_df = pd.DataFrame(
    pd.read_csv(os.path.join(data_directory, dfs_to_join[0]), index_col=0)
)

for df_path in dfs_to_join[1:]:
    df = pd.read_csv(os.path.join(data_directory, df_path), index_col=0)
    cluster_df = pd.merge(cluster_df, df, on=["Year", "Borough"], how="inner")

cluster_df = cluster_df.pivot(index="Year", columns="Borough")
cluster_df = cluster_df.fillna(method="ffill").fillna(method="bfill")


def get_pas_pivot_dict() -> dict[str, dict[str, list[pd.Timestamp]]]:
    df = pd.read_csv(os.path.join(data_directory, "pas_data_pivots.csv"))
    df["pivot"] = pd.to_datetime(df["pivot"])

    # Group by borough and measure and aggregate timestamps
    grouped = df.groupby(["borough", "measure"])["pivot"].apply(list).reset_index()

    # Convert the grouped DataFrame to the nested dictionary format
    result_dict = {}
    for _, row in grouped.iterrows():
        borough = row["borough"]
        measure = row["measure"]
        timestamps = row["pivot"]

        if borough not in result_dict:
            result_dict[borough] = {}
        result_dict[borough][measure] = timestamps

    return result_dict


pas_pivot_data = get_pas_pivot_dict()

side_bar = html.Div(
    html.Div(
        [
            dcc.Store(id="recommendations-store"),
            html.H4(
                "Clustering",
                style={"padding": "10px", "border-bottom": "1px solid white"},
            ),
            dcc.Dropdown(
                id="column-selection",
                options=cluster_df.columns.levels[0],
                value=cluster_df.columns.levels[0],
                multi=True,
                placeholder="Select columns to cluster on",
                style={"margin-bottom": "15px"},
            ),
            html.Button(
                "Generate suggestions",
                id="generate-button",
                n_clicks=0,
                style={"margin-bottom": "15px"},
            ),
            dcc.Loading(
                id="loading",
                type="default",
                children=[
                    dcc.Dropdown(
                        id="borough-selection",
                        placeholder="Select Borough",
                        style={"margin-bottom": "15px"},
                        options=[
                            {"label": col, "value": col}
                            for col in pas_pivot_data.keys()
                        ],
                        disabled=True,
                    ),
                    dcc.Dropdown(
                        id="measure-selection",
                        placeholder="Select Measure",
                        style={"margin-bottom": "15px"},
                        options=[
                            {"label": borough, "value": borough}
                            for borough in pas_pivot_data.keys()
                        ],
                        disabled=True,
                    ),
                    html.Div(id="graphs-container"),
                ],
            ),
        ],
        className="slide-in-content",
        id="slide-in-content",
    ),
    className="slide-in",
    id="slide-in",
)


@dash.callback(
    Output("recommendations-store", "data"),
    Output("borough-selection", "options"),
    Output("borough-selection", "disabled"),
    # also set the disabled state of the measure selection and set selected borough to None
    Output("borough-selection", "value"),
    Input("generate-button", "n_clicks"),
    State("column-selection", "value"),
)
def generate_recommendations(n_clicks, selected_columns):
    if n_clicks == 0 or not selected_columns:
        return [], [], True, None

    recommendations: list[Recommendation] = []

    for borough, metrics_with_pivot_timestamps in pas_pivot_data.items():
        for metric, pivot_timestamps in metrics_with_pivot_timestamps.items():
            for timestamp in pivot_timestamps:
                df_before_timestamp = cluster_df.loc[cluster_df.index < timestamp.year][
                    selected_columns
                ]

                X = to_time_series_dataset(
                    [
                        df_before_timestamp.xs(borough, axis=1, level="Borough").values
                        for borough in df_before_timestamp.columns.get_level_values(
                            "Borough"
                        ).unique()
                    ]
                )

                scaler = TimeSeriesScalerMeanVariance()
                X = scaler.fit_transform(X)

                n_clusters = 5

                model = TimeSeriesKMeans(
                    n_clusters=n_clusters,
                    metric="euclidean",
                    max_iter=20,
                    random_state=42,
                )

                # Fit the model
                y_pred = model.fit_predict(X)

                borough_predictions = dict(
                    zip(
                        df_before_timestamp.columns.get_level_values(
                            "Borough"
                        ).unique(),
                        y_pred,
                    )
                )

                current_borough_cluster = borough_predictions[borough]

                for borough_to_compare in df_before_timestamp.columns.get_level_values(
                    "Borough"
                ).unique():
                    if borough == borough_to_compare:
                        continue

                    try:
                        value_at_pivot = (
                            cluster_df.loc[cluster_df.index == timestamp.year]
                            .xs(borough, axis=1, level="Borough")[metric]
                            .values[0]
                        )
                    except IndexError:
                        print(metric)
                        continue

                    last_value = cluster_df.xs(borough, axis=1, level="Borough")[
                        metric
                    ].values[-1]

                    if (
                        borough_predictions[borough_to_compare]
                        == current_borough_cluster  # borough and borough_to_compare are in the same cluster
                        and last_value
                        > value_at_pivot
                        + 0.005  # last value is higher than at the pivot
                    ):
                        recommendations.append(
                            {
                                "borough": borough,
                                "metric": metric,
                                "borough_to_compare": borough_to_compare,
                                # compute euclidian distance between the two boroughs for all columns used in clustering
                                "distance": np.linalg.norm(
                                    df_before_timestamp.xs(
                                        borough, axis=1, level="Borough"
                                    )
                                    - df_before_timestamp.xs(
                                        borough_to_compare, axis=1, level="Borough"
                                    )
                                ),
                                "pivot_point": timestamp.isoformat(),
                            }
                        )

    # get available boroughs from recommendations
    suggested_boroughs = set()

    for recommendation in recommendations:
        suggested_boroughs.add(recommendation["borough"])

    return recommendations, list(suggested_boroughs), False, None


# get available measures for selected borough
@dash.callback(
    Output("measure-selection", "options"),
    Output("measure-selection", "disabled"),
    Input("borough-selection", "value"),
    State("recommendations-store", "data"),
)
def update_measure_selection(borough, recommendations):
    if not borough:
        return [], True

    available_measures = set()

    for recommendation in recommendations:
        if recommendation["borough"] == borough:
            available_measures.add(recommendation["metric"])

    return (
        [{"label": measure, "value": measure} for measure in available_measures],
        False,
    )


@dash.callback(
    Output("graphs-container", "children"),
    [
        Input("borough-selection", "value"),
        Input("measure-selection", "value"),
        Input("recommendations-store", "data"),
    ],
)
def plot_charts(borough, measure, recommendations: list[Recommendation]):
    if not borough or not measure:
        return []

    # Filter recommendations
    filtered_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation["borough"] == borough and recommendation["metric"] == measure
    ]

    if not filtered_recommendations:
        return []

    # Create a graph for each filtered recommendation
    graphs = []
    for i, rec in enumerate(filtered_recommendations):
        fig = go.Figure()

        series = cluster_df.xs(rec["borough"], axis=1, level="Borough")[rec["metric"]]
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series.values,
                mode="lines",
                name=rec["borough"],
            )
        )

        # plot pivot point
        fig.add_vline(
            x=pd.to_datetime(rec["pivot_point"]).year,
            line_dash="dash",
            line_color="red",
            annotation_text="Pivot",
            annotation_position="top left",
        )

        fig.update_layout(
            title=f"{rec['borough']} and {rec['borough_to_compare']} - {measure} - {rec['distance']:.2f}",
            xaxis_title="Date",
            yaxis_title=measure,
        )

        graph = dcc.Graph(id=f"time-series-plot-{i}", figure=fig)
        graphs.append(graph)

    return graphs


@dash.callback(
    Output("sidebar-column", "width"),
    [Input("sidebar-button", "n_clicks")],
    [State("slide-in", "className")],
)
def update_sidebar_width(n_clicks, sidebar_class):
    if "show" in sidebar_class:  # If the sidebar is expanded
        return 2  # Adjust sidebar width
    else:
        return 3  # Default sidebar width


@dash.callback(
    Output("slide-in", "className"),
    [Input("sidebar-button", "n_clicks")],
    [State("slide-in", "className")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def toggle_slide_in(opened, current_class):
    if opened % 2 == 1:
        return f"{current_class} show"  # Show the sidebar by adding the 'show' class
    else:
        return current_class.replace("show", "")
