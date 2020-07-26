import pandas as pd
import numpy as np

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
# import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# import plotly.express as px
# import plotly.graph_objects as go
# import time
# import datetime
# #import torch
# from transformers import MarianMTModel, MarianTokenizer
#import nltk
# from typing import List
# import json
# import plotly
# from newsapi import NewsApiClient
# import urllib.request as requests

app = dash.Dash()
app.title = "Multilingual Covid-19 Dashboard"

app_name = "Multilingual Covid-19 Dashboard" 

server = app.server

app.layout = html.Div("Testing")