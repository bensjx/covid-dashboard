# Import general libraries
import pandas as pd
import numpy as np
import pprint
import datetime
import random
import os
import psycopg2

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly
import plotly.express as px

# Other tabs
from analysis import analysisTab
from news import newsTab
from socialMedia import socialMediaTab
from info import infoTab
import parameters

# For socialMedia.py
import mysql.connector
from nltk.tokenize import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.title = "Dengue Dashboard"

app_name = "Dengue Dashboard"

server = app.server

DENGUE_LOGO = "https://image.flaticon.com/icons/svg/3055/3055410.svg"

# Navigation bar
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
            href="https://dengue-db.herokuapp.com/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
    style={"width": "100%"},
)

# Layout of entire app
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

##### For socialMedia.py
# Sentiment analysis line chart and pie chart
@app.callback(
    Output("sa-graph", "children"), [Input("interval-component-slow", "n_intervals")]
)
def sa_line(n):
    # db_connection = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="password",
    #     database="TwitterDB",
    #     charset="utf8",
    # )

    # Loading data from Heroku PostgreSQL
    DATABASE_URL = os.environ["DATABASE_URL"]
    db_connection = psycopg2.connect(DATABASE_URL, sslmode="require")

    # Load last 24 hour data from MySQL
    timenow = (
        datetime.datetime.now()
        - datetime.timedelta(hours=0, minutes=parameters.TIME_PERIOD_MIN)
    ).strftime("%Y-%m-%d %H:%M:%S")

    query = "SELECT id_str, clean_text, text, created_at, polarity FROM {} WHERE created_at >= '{}' ".format(
        "dengue", timenow
    )

    df = pd.read_sql(query, con=db_connection)

    # Convert UTC into SGT
    df["created_at"] = pd.to_datetime(df["created_at"]).apply(
        lambda x: x + datetime.timedelta(hours=8)
    )

    # Clean and transform data to enable time series
    # Bin into 5 minutes
    result = (
        df.groupby([pd.Grouper(key="created_at", freq="5min"), "polarity"])
        .count()
        .reset_index()
    )
    result = result.rename(
        columns={
            "id_str": "Num of '{}' mentions".format(parameters.TRACK_WORDS[0]),
            "created_at": "Time",
        }
    )
    time_series = result["Time"][result["polarity"] == 0].reset_index(drop=True)

    past_x_min = datetime.datetime.now() - datetime.timedelta(
        minutes=parameters.TIME_PERIOD_MIN
    )

    neu_num = result[result["Time"] > past_x_min][
        "Num of '{}' mentions".format(parameters.TRACK_WORDS[0])
    ][result["polarity"] == 0].sum()
    neg_num = result[result["Time"] > past_x_min][
        "Num of '{}' mentions".format(parameters.TRACK_WORDS[0])
    ][result["polarity"] == -1].sum()
    pos_num = result[result["Time"] > past_x_min][
        "Num of '{}' mentions".format(parameters.TRACK_WORDS[0])
    ][result["polarity"] == 1].sum()

    # Word cloud
    tknzr = TweetTokenizer()
    full_words = tknzr.tokenize(" ".join([i for i in df.text]))
    full_words_sw = [
        word for word in full_words if word not in stopwords.words("english")
    ]
    counted = Counter(full_words_sw)
    words = [tup[0] for tup in counted.most_common()[:50]]
    colors = [
        plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)]
        for i in range(len(words))
    ]
    full_weights = [tup[1] for tup in counted.most_common()[: len(words)]]
    weights = [i for i in range(15, 35)][::-1] + ([15] * (len(words) - (35 - 15)))
    wc_data = pd.DataFrame(
        {
            "words": words,
            "color": colors,
            "weights": weights,
            "x": random.choices(range(len(words)), k=len(words)),
            "y": random.choices(range(len(words)), k=len(words)),
            "freq": full_weights,
        }
    )

    children = html.Div(
        [
            dbc.Row(
                [
                    # line chart
                    dcc.Graph(
                        id="sa-line-chart",
                        figure={
                            "data": [
                                go.Scatter(
                                    x=time_series,
                                    y=result[
                                        "Num of '{}' mentions".format(
                                            parameters.TRACK_WORDS[0]
                                        )
                                    ][result["polarity"] == 0].reset_index(drop=True),
                                    name="Neutrals",
                                    opacity=0.8,
                                    mode="lines",
                                    line=dict(width=0.5, color="rgb(0, 128, 155)"),
                                    stackgroup="one",
                                ),
                                go.Scatter(
                                    x=time_series,
                                    y=result[
                                        "Num of '{}' mentions".format(
                                            parameters.TRACK_WORDS[0]
                                        )
                                    ][result["polarity"] == -1]
                                    .reset_index(drop=True)
                                    .apply(lambda x: -x),
                                    name="Negatives",
                                    opacity=0.8,
                                    mode="lines",
                                    line=dict(width=0.5, color="rgb(255, 128, 128)"),
                                    stackgroup="two",
                                ),
                                go.Scatter(
                                    x=time_series,
                                    y=result[
                                        "Num of '{}' mentions".format(
                                            parameters.TRACK_WORDS[0]
                                        )
                                    ][result["polarity"] == 1].reset_index(drop=True),
                                    name="Positives",
                                    opacity=0.8,
                                    mode="lines",
                                    line=dict(width=0.5, color="rgb(181, 230, 29)"),
                                    stackgroup="three",
                                ),
                            ],
                            "layout": {
                                "width": "900",
                                "title": "Plot of sentiments every 5 minutes",
                            },
                        },
                    ),
                    # pie chart
                    dcc.Graph(
                        id="pie-chart",
                        figure={
                            "data": [
                                go.Pie(
                                    labels=["Positives", "Negatives", "Neutrals"],
                                    values=[pos_num, neg_num, neu_num],
                                    marker_colors=[
                                        "rgb(181, 230, 29)",
                                        "rgb(255, 128, 128)",
                                        "rgb(0, 128, 155)",
                                    ],
                                    textinfo="value",
                                    hole=0.55,
                                )
                            ],
                            "layout": {
                                "showlegend": False,
                                "title": "Sentiment of Tweets In the Last {} Mins".format(
                                    parameters.TIME_PERIOD_MIN
                                ),
                                "annotations": [
                                    dict(
                                        text="{}".format((pos_num + neg_num + neu_num)),
                                        font=dict(size=30),
                                        showarrow=False,
                                    )
                                ],
                                "height": 400,
                                "width": 400,
                            },
                        },
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    # Actual Tweets
                    html.Div(
                        children=[
                            html.H5("Actual Tweets", style={"textAlign": "center"}),
                            dash_table.DataTable(
                                id="tweet_table",
                                columns=[
                                    {"name": i, "id": i}
                                    for i in ["created_at", "clean_text"]
                                ],
                                data=df.iloc[::-1].to_dict("records"),
                                page_size=10,
                                style_cell={
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "textAlign": "left",
                                },
                                tooltip_data=[
                                    {
                                        column: {
                                            "value": str(value),
                                            "type": "markdown",
                                        }
                                        for column, value in row.items()
                                    }
                                    for row in df.iloc[::-1].to_dict("rows")
                                ],
                            ),
                        ],
                        style={
                            "marginLeft": 40,
                            "width": "50%",
                            # "display": "inline-block",
                        },
                    ),
                    # Word Cloud
                    html.Div(
                        dcc.Graph(
                            id="wc-graph",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=wc_data.x,
                                        y=wc_data.y,
                                        mode="text",
                                        text=wc_data.words,
                                        marker={"opacity": 0.3},
                                        hoverinfo="text",
                                        hovertext=[
                                            "{0}: {1}".format(w, f)
                                            for w, f in zip(wc_data.words, wc_data.freq)
                                        ],
                                        textfont={
                                            "size": wc_data.weights,
                                            "color": wc_data.color,
                                        },
                                    ),
                                ],
                                "layout": go.Layout(
                                    {
                                        "xaxis": {
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "zeroline": False,
                                        },
                                        "yaxis": {
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "zeroline": False,
                                        },
                                        "title": "Word Cloud",
                                    }
                                ),
                            },
                        ),
                        style={"width": "40%",},
                    ),
                ]
            ),
        ]
    )
    return children


if __name__ == "__main__":
    app.run_server(debug=False)
