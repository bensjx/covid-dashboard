# Dengue-dashboard

Deployed app here: https://dengue-db.herokuapp.com/

How it's made: https://towardsdatascience.com/@bensjyy

This application aims to provide intelligence on a niche topic with the following 3 features:

1. Analysis: Visualise the number of dengue cases, along with an overlayed map of dengue hot zones and breeding spots.
1. News: This tab is able to retrieve news from multiple sources regarding "Dengue".
1. Twitter Analysis: There are 4 charts:
   - A line chart showing how sentiment of tweets related to "dengue" is changing every 5 minutes
   - A pie chart showing the proportion of sentiments for tweets related to "dengue"
   - A table to gather live tweets
   - A word cloud to visualise frequently occuring words

# Concepts:

1. Dash by Plotly - Web framework in Python
1. Heroku - Deployment of web application
1. Newsapi - Fetch news from a variety of sources
1. Folium - Geospatial analytics
1. Tweepy - Twitter Data Scraping
1. TextBlob - Sentiment Analysis
1. PostgreSQL - Database for scraping and retrieval

# Resources:

1. Data:
   - https://data.gov.sg/dataset/dengue-clusters
   - https://data.gov.sg/dataset/areas-with-high-aedes-population
1. Deploying with Heroku: https://www.youtube.com/watch?v=j3VvVaNnDH4&t=480s
1. DBC: https://dash-bootstrap-components.opensource.faculty.ai/
1. DCC: https://dash.plotly.com/dash-core-components
1. Newsapi: https://newsapi.org/
1. Folium: https://blog.algorexhealth.com/2018/04/everything-you-never-wanted-to-know-about-geographic-charting/
1. Folium integration: https://medium.com/@shachiakyaagba_41915/integrating-folium-with-dash-5338604e7c56
1. Inspiration: https://github.com/nagarajbhat/dash-covid19-multilingual
1. Tweepy Guide: https://github.com/Chulong-Li/Real-time-Sentiment-Tracking-on-Twitter-for-Brand-Improvement-and-Trend-Recognition

# Setup:

1. Create an anaconda enviornment with python=3.6
1. Update your environment with `conda env update -n <environment name> -f environment.yml --prune`
   - If update fails follow this script: https://stackoverflow.com/questions/35802939/install-only-available-packages-using-conda-install-yes-file-requirements-t
1. If `fiona` package has an error, follow (source: https://stackoverflow.com/questions/54734667/error-installing-geopandas-a-gdal-api-version-must-be-specified-in-anaconda
   ):
   - `conda remove gdal fiona pyproj six rtree geopandas`
   - `pip install pipwin`
   - `pipwin install gdal fiona pyproj six rtree geopandas`
1. Clone this repo
