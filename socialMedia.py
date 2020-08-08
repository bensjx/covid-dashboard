# Import general libraries
import pandas as pd
import numpy as np
import os

# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Tweepy
import tweepy as tw

# Retrieve keys
try:  # retrieve from local system
    from keys import (
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_token_secret,
    )

    auth = tw.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
except:  # retrieve from Heroku
    twitter_consumer_key = os.environ["twitter_consumer_key"]
    twitter_consumer_secret = os.environ["twitter_consumer_secret"]
    twitter_access_token = os.environ["twitter_access_token"]
    twitter_access_token_secret = os.environ["twitter_access_token_secret"]

    auth = tw.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)


search_term = "dengue -filter:retweets"

tweets = tw.Cursor(api.search, q=search_term, lang="en", since="2018-04-23").items(10)

all_tweets = [tweet.text for tweet in tweets]
all_tweets[:5]

socialMediaTab = None
