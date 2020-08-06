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
from branca.element import Template, MacroElement


def calc_cases():
    central_data = gpd.read_file("data/dengue-cases-central-geojson.geojson")
    ne_data = gpd.read_file("data/dengue-cases-north-east-geojson.geojson")
    se_data = gpd.read_file("data/dengue-cases-south-east-geojson.geojson")
    sw_data = gpd.read_file("data/dengue-cases-south-west-geojson.geojson")

    central_cases = sum(
        central_data.Description.map(
            lambda x: int(re.search(r"(<td>.*?</td>)", x).group(0)[4:-5])
        )
    )
    ne_cases = sum(
        ne_data.Description.map(
            lambda x: int(re.search(r"(<td>.*?</td>)", x).group(0)[4:-5])
        )
    )
    se_cases = sum(
        se_data.Description.map(
            lambda x: int(re.search(r"(<td>.*?</td>)", x).group(0)[4:-5])
        )
    )
    sw_cases = sum(
        sw_data.Description.map(
            lambda x: int(re.search(r"(<td>.*?</td>)", x).group(0)[4:-5])
        )
    )
    total_cases = sum([central_cases, ne_cases, se_cases, sw_cases])

    return [total_cases, central_cases, ne_cases, se_cases, sw_cases]


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

    # Legend
    # Template from: https://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd
    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>Legend</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:#73adff;opacity:0.9;'></span>Dengue clusters</li>
        <li><span style='background:#FF0000;opacity:0.7;'></span>Areas with high ades population</li>

    </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)
    m.get_root().add_child(macro)

    m.save("dengue-cluster.html")
    return m


# map_graph()

analysisTab = dbc.Card(
    [
        dbc.CardBody(
            [
                # Overview
                html.P("Accurate as of: 02 Aug 2020"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(id="case_1", children=["Total Cases"],)
                                    ),
                                    dbc.CardBody(html.H4(calc_cases()[0])),
                                ],
                                color="danger",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="case_2", children=["Central Cases"],
                                        )
                                    ),
                                    dbc.CardBody(html.H4(calc_cases()[1])),
                                ],
                                color="secondary",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="case_3", children=["North-East Cases"],
                                        )
                                    ),
                                    dbc.CardBody(html.H4(calc_cases()[2])),
                                ],
                                color="success",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="case_4", children=["South-East Cases"],
                                        )
                                    ),
                                    dbc.CardBody(html.H4(calc_cases()[3])),
                                ],
                                color="warning",
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H6(
                                            id="case_5", children=["South-West Cases"],
                                        )
                                    ),
                                    dbc.CardBody(html.H4(calc_cases()[4])),
                                ],
                                color="info",
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
                # #
                # dbc.Spinner(
                #     color="primary",
                #     type="grow",
                #     children=[dcc.Graph(id="graph_compare_country")],
                # ),
                # html.Br(),
            ]
        )
    ]
)

