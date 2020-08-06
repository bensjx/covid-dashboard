import pandas as pd
import numpy as np
import pprint

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from analysis import analysisTab
from news import newsTab
from socialMedia import socialMediaTab
from info import infoTab

# import plotly.express as px
# import plotly.graph_objects as go
# import time
# import datetime
# #import torch
# from transformers import MarianMTModel, MarianTokenizer
# import nltk
# from typing import List
# import json
# import plotly
# from newsapi import NewsApiClient
# import urllib.request as requests

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.title = "Dengue Dashboard"

app_name = "Dengue Dashboard"

server = app.server

DENGUE_LOGO = "https://image.flaticon.com/icons/svg/3055/3055410.svg"

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=DENGUE_LOGO, height="50px")),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Dengue Analysis",
                            className="ml-auto",
                            style={"font-size": 30},
                        )
                    ),
                ],
                align="left",
                no_gutters=True,
            ),
            href="https://dengue-db-ben.herokuapp.com/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
    style={"width": "100%"},
)


app.layout = html.Div(
    [
        navbar,
        dbc.Tabs(
            [
                dbc.Tab(analysisTab, id="label_tab1", label="Visuals"),
                dbc.Tab(newsTab, id="label_tab2", label="Related News"),
                dbc.Tab(socialMediaTab, id="label_tab3", label="Twitter Analysis"),
                dbc.Tab(infoTab, id="label_tab4", label="More Information"),
            ],
            style={"font-size": 20, "background-color": "#b9d9eb"},
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
