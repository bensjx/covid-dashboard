# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

infoTab = dbc.Card(
    dbc.CardBody(
        [
            # Generic Info
            dbc.Row(dbc.Card(html.H6("Created cause got data but not visualised. Also not overlayed"))),
            # Something else
            dbc.Row(dbc.Card(html.H6("smt else"))),
        ]
    )
)
