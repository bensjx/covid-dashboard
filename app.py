import pandas as pd
import numpy as np
import pprint

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from analysis import *
from news import *
from socialMedia import *
from controls import *

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

app.title = "Multilingual Covid-19 Dashboard"

app_name = "Multilingual Covid-19 Dashboard"

server = app.server

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(dbc.Button("Search", color="primary", className="ml-2"), width="auto",),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

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
                            "Dengue Analysis", className="ml-2", style={"font-size": 25}
                        )
                    ),
                ],
                align="left",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
)


app.layout = html.Div(
    [
        navbar,
        dbc.Tabs(
            [
                dbc.Tab(analysistab, id="label_tab1", label="Analysis"),
                dbc.Tab(newstab, id="label_tab2", label="News"),
            ]
        ),
    ]
)

# app.layout = dbc.Container([
#             dbc.Row(navbar),

#           dbc.Tabs([
#                  dbc.Tab(tab1, id="label_tab1",label='Analysis'),
#                  dbc.Tab(tab2, id="label_tab2",label='News')

#         ])
#         ],
#             fluid=True
# )


# @app.callback(Output('news_all','children'))
# def news_update():
#     all_articles = newsapi.get_everything(q='dengue singapore',
#                                       from_param=date_n_days_ago,
#                                       to=date_now,
#                                       language='en',
#                                       sort_by='relevancy',
#                                     )

#     all_articles_title = [str(all_articles['articles'][i]['title']) for i in range(len(all_articles['articles']))]
#     all_articles_url = [all_articles['articles'][i]['url'] for i in range(len(all_articles['articles']))]
#     # all_articles_source = [str(all_articles['articles'][i]['source']['name']) for i in range(len(all_articles['articles']))]
#     all_articles_content = [str(all_articles['articles'][i]['content']).split("[")[0] for i in range(len(all_articles['articles']))]
#     all_articles_description = [str(all_articles['articles'][i]['description']) for i in range(len(all_articles['articles']))]
#     all_articles_date =  [str(datetime.datetime.date(pd.to_datetime(all_articles['articles'][i]['publishedAt']))) for i in range(len(all_articles['articles']))]
#     all_articles_img =  [str(all_articles['articles'][i]['urlToImage']) for i in range(len(all_articles['articles']))]

#     news_all = [dbc.Card(
#         [
#             dbc.CardImg(src=all_articles_img[i], top=True),
#             dbc.CardBody(
#                 [
#                     html.H4(all_articles_title, className="card-title"),
#                     html.P(
#                         all_articles_description,
#                         className="card-text",
#                     ),
#                     dbc.Button("Source", color="primary"),
#                 ]
#             ),
#         ],
#         style={"width": "18rem"},
#     ) for i in range(len(all_articles))]

#     # news_all= [dbc.Card([
#     #             dbc.CardHeader([html.A(id="news_title_url",children=[top_headlines_title[i]],href=top_headlines_url[i])
#     #                                 ,html.P("|"+top_headlines_source[i]+"|"+top_headlines_date[i])]),
#     #             dbc.CardBody([html.P(id="news_source",children=top_headlines_description[i]),
#     #                           html.Img(src=top_headlines_img[i],alt="image",style={
#     #                             'max-width': '70%','max-height': '70%',
#     #                             'margin': 'auto','display': 'block'}
#     #                             )]),
#     #             ],
#     #             color='secondary',style={"max-width":300,"height":400,"display":"flex","float":"left",  "margin": 20}) for i in range(len(all_articles))]

#     return news_all

if __name__ == "__main__":
    app.run_server(debug=True)
