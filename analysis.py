# General libraries
import pandas as pd
import numpy as np
import json
import pprint
import regex as re

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Plotting libraries
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Polygon


def map_graph():
    # GeoJson Data
    cluster_gj = gpd.read_file("data/dengue-clusters-geojson.geojson")
    area_high_ades_gj = gpd.read_file(
        "data/areas-with-high-aedes-population-geojson.geojson"
    )

    # Creation of map
    kw = {"location": [1.3521, 103.8198], "zoom_start": 12}
    m = folium.Map(**kw)

    # Styles
    area_high_ades_style = {"fillColor": "#228B22", "color": "#FF0000"}

    # Modifying tooltip
    cluster_gj.Description = cluster_gj.Description.map(
        lambda x: re.search(r"(<td>.*?</td>)", x).group(0)[4:-5]
    )

    area_high_ades_gj.Description = area_high_ades_gj.Description.map(
        lambda x: re.search(r"(<td>.*?</td>)", x).group(0)[4:-5]
    )

    # Addition of layers to map
    folium.GeoJson(
        cluster_gj,
        tooltip=folium.GeoJsonTooltip(
            fields=["Description"], aliases=["Location"], localize=True
        ),
    ).add_to(m)

    folium.GeoJson(
        area_high_ades_gj,
        style_function=lambda x: area_high_ades_style,
        tooltip=folium.GeoJsonTooltip(
            fields=["Description"], aliases=["Location"], localize=True
        ),
    ).add_to(m)

    m.save("dengue-cluster.html")
    return m


map_graph()

analysisTab = dbc.Card(
    [
        dbc.CardBody(
            [
                # Overview
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info1",
                                            children=["location country"],
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="location_country")),
                                ],
                                color="info",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(id="label_info2", children=["date"])
                                    ),
                                    dbc.CardBody(html.H4(id="date")),
                                ],
                                color="info",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info3", children=["Total cases"]
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="total_cases")),
                                ],
                                color="warning",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info4", children=["New cases"]
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="new_cases")),
                                ],
                                color="warning",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info5", children=["total deaths"]
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="total_deaths")),
                                ],
                                color="danger",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info6", children=["New deaths"]
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="new_deaths")),
                                ],
                                color="danger",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info7", children=["total tests"]
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="total_tests")),
                                ],
                                color="success",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="label_info8", children=["New tests"]
                                        )
                                    ),
                                    dbc.CardBody(html.H4(id="new_tests")),
                                ],
                                color="success",
                            )
                        ),
                    ]
                ),
                html.Br(),
                ## Graphs
                # Dengue cluster
                html.P("Accurate as of: 02 Aug 2020"),
                html.Iframe(
                    id="dengue-map",
                    srcDoc=open("dengue-cluster.html", "r").read(),
                    width="100%",
                    height="500",
                ),
                html.Br(),
                #
                dbc.Spinner(
                    color="primary",
                    type="grow",
                    children=[dcc.Graph(id="graph_treemap_continent")],
                ),
                html.Br(),
                #
                dbc.Spinner(
                    color="primary",
                    type="grow",
                    children=[dcc.Graph(id="graph_bar_continent")],
                ),
                html.Br(),
                #
                dbc.Spinner(
                    color="primary",
                    type="grow",
                    children=[dcc.Graph(id="graph_line_continent")],
                ),
                html.Br(),
                #
                dbc.Spinner(
                    color="primary",
                    type="grow",
                    children=[dcc.Graph(id="graph_area_continent")],
                ),
                html.Br(),
                #
                dbc.Spinner(
                    color="primary",
                    type="grow",
                    children=[dcc.Graph(id="graph_compare_country")],
                ),
                html.Br(),
                # #
                # html.H6(
                #     id="label_not_translated",
                #     children=[
                #         "If any text in this dashboard is untranslated, type or copy paste it here this to translate!"
                #     ],
                # ),
                # dcc.Input(id="input_text", type="text", placeholder=""),
                # html.Button("Translate", id="submit-val"),
                # dbc.Spinner(
                #     color="primary", type="grow", children=[html.Div(id="output_text")]
                # ),
            ]
        )
    ]
)

