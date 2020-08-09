# Import general libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pprint
import os

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Import newsapi
from newsapi import NewsApiClient

try:
    from keys import newsapikey  # retrieve from local system

    newsapi = NewsApiClient(api_key=newsapikey)
except:
    newsapikey = os.environ["newapi_key"]  # retrieve from Heroku
    newsapi = NewsApiClient(api_key=newsapikey)

n_days_ago = 30
date_n_days_ago = datetime.now() - timedelta(days=n_days_ago)
date_now = datetime.now()


def news_update():
    all_articles = newsapi.get_everything(
        q="dengue singapore",
        from_param=date_n_days_ago,
        to=date_now,
        language="en",
        sort_by="publishedAt",
        page_size=100,
    )

    all_articles_title = [
        str(all_articles["articles"][i]["title"])
        for i in range(len(all_articles["articles"]))
    ]
    all_articles_url = [
        all_articles["articles"][i]["url"] for i in range(len(all_articles["articles"]))
    ]
    all_articles_description = [
        str(all_articles["articles"][i]["description"])
        for i in range(len(all_articles["articles"]))
    ]
    all_articles_date = [
        str(datetime.date(pd.to_datetime(all_articles["articles"][i]["publishedAt"])))
        for i in range(len(all_articles["articles"]))
    ]
    all_articles_img = [
        str(all_articles["articles"][i]["urlToImage"])
        for i in range(len(all_articles["articles"]))
    ]

    news_all = []
    temp_news = []
    col = ["warning", "success", "info", "success"]
    col_idx = 0

    for i in range(len(all_articles["articles"])):
        temp_news.append(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(
                            src=all_articles_img[i],
                            top=True,
                            style={
                                "max-width": "80%",
                                "max-height": 200,
                                "margin": "auto",
                                "display": "block",
                                "padding-top": "10px",
                            },
                        ),
                        dbc.CardBody(
                            [
                                html.H4(all_articles_title[i], className="card-title"),
                                html.P(
                                    all_articles_description[i],
                                    className="card-text",
                                    # style={"fontSize": 16}
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            [
                                all_articles_date[i],
                                dbc.Button(
                                    "Source",
                                    color="primary",
                                    href=all_articles_url[i],
                                    style={"float": "right"},
                                ),
                            ]
                        ),
                    ],
                    color=col[col_idx],
                    style={"height": 525},
                )
            )
        )

        col_idx += 1
        if col_idx > 3:
            col_idx = 0

        if (i + 1) % 3 == 0:
            news_all.append(
                dbc.Row(temp_news, className="mb-4", style={"padding": "1em"})
            )
            temp_news = []

    return news_all


newsTab = html.Div(news_update())
