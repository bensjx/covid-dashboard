# Import general libraries
import pandas as pd
import numpy as np
import json
import os

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

socialMediaTab = html.Div(
    children=[
        html.H2("Real-time Twitter Analysis on Dengue", style={"textAlign": "center"}),
        html.Div(
            "Note: Tweets have been translated from various languages due to the lack of english tweets. Location is set to \
                worldwide due to the lack of tweets from Singapore."
        ),
        html.Br(),
        html.Div(id="sa-graph"),
        html.Br(),
        dcc.Interval(
            id="interval-component-slow",
            interval=1 * 30000,  # in milliseconds, aka refreshes every 30 seconds
            n_intervals=0,
        ),
    ],
    style={"padding": "20px"},
)
